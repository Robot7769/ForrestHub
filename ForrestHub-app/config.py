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
    GAMES_DIR_LIVE = "ForrestHub-games"
    ASSETS_DIR = "assets"
    PAGES_DIR = "pages"

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
    TEMPLATES_FOLDER = Path(DATA_DIR) / TEMPLATES_DIR
    GAMES_FOLDER = Path(DATA_DIR) / GAMES_DIR
    ASSETS_FOLDER = Path(DATA_DIR) / ASSETS_DIR
    PAGES_FOLDER = Path(DATA_DIR) / PAGES_DIR

    LIVE_GAMES_MODE = False
    GAMES_FOLDER_LIVE = Path(EXECUTABLE_DIR) / GAMES_DIR_LIVE

    if GAMES_FOLDER_LIVE.exists():
        LIVE_GAMES_MODE = True

    # Disable debug and reloader when using frozen data with live data - production mode
    if not LIVE_GAMES_MODE and FROZEN:
        DEBUG = False
        USE_RELOADER = False
