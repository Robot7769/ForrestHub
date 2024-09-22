import os
import sys
from app.utils import get_local_ip_address
from pathlib import Path


class Config:
    VERSION = "1.2.3"
    DATAFILE = "ForrestHub-data.json"
    LOG_FOLDER = "ForrestHub-logs"
    ALLOWED_EXTENSIONS = ["json"]
    TEMPLATES_DIR = "templates"
    GAMES_DIR = "games"
    ASSETS_DIR = "assets"

    LIVE_DATA_DIR = "forrestHub-live"
    IP_ADDRESS = get_local_ip_address()

    DEBUG = True
    USE_RELOADER = True

    if getattr(sys, "frozen", False):
        FROZEN = True
        PORT = 80
        EXECUTABLE_DIR = Path(sys.executable).parent
        DATA_DIR = sys._MEIPASS
    else:
        FROZEN = False
        PORT = 4444
        EXECUTABLE_DIR = Path(__file__).parent
        DATA_DIR = EXECUTABLE_DIR

    # use live data if it exists
    LIVE_DATA_FOLDER = Path(EXECUTABLE_DIR) / LIVE_DATA_DIR
    TEMPLATES_FOLDER = Path(DATA_DIR) / TEMPLATES_DIR
    GAMES_FOLDER = Path(DATA_DIR) / GAMES_DIR
    ASSETS_FOLDER = Path(DATA_DIR) / ASSETS_DIR
    LIVE_DATA_USED = False

    if LIVE_DATA_FOLDER.exists():
        LIVE_DATA_USED = True
        TEMPLATES_FOLDER_LIVE = Path(LIVE_DATA_FOLDER) / TEMPLATES_DIR
        GAMES_FOLDER_LIVE = Path(LIVE_DATA_FOLDER) / GAMES_DIR
        ASSETS_FOLDER_LIVE = Path(LIVE_DATA_FOLDER) / ASSETS_DIR

        # check if exist
        if not TEMPLATES_FOLDER_LIVE.exists():
            raise FileNotFoundError(f"Templates folder not found: {TEMPLATES_FOLDER}")

        if not GAMES_FOLDER_LIVE.exists():
            raise FileNotFoundError(f"Games folder not found: {GAMES_FOLDER}")

        if not ASSETS_FOLDER_LIVE.exists():
            raise FileNotFoundError(f"Assets folder not found: {ASSETS_FOLDER}")

    # Disable debug and reloader when using frozen data with live data - production mode
    if not LIVE_DATA_USED and FROZEN:
        DEBUG = False
        USE_RELOADER = False
