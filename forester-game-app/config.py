import os
import sys
from app.utils import get_local_ip_address
import pathlib


class Config:
    VERSION = "1.1.0"
    DATAFILE = "data.json"
    LOG_FOLDER = "ForesterLogs"
    ALLOWED_EXTENSIONS = ["json"]
    TEMPLATES_DIR = "templates"
    GAMES_DIR = "games"
    ASSETS_DIR = "assets"

    LIVE_DATA_DIR = "forester-live"
    IP_ADDRESS = get_local_ip_address()

    DEBUG = True
    USE_RELOADER = True

    if getattr(sys, "frozen", False):
        FROZEN = True
        PORT = 80
        ROOT_DIR = pathlib.Path(sys.executable).parent
        DATA_DIR = sys._MEIPASS
    else:
        FROZEN = False
        PORT = 4444
        ROOT_DIR = pathlib.Path(__file__).parent
        DATA_DIR = ROOT_DIR

    # use live data if it exists
    LIVE_DATA_FOLDER = pathlib.Path(ROOT_DIR) / LIVE_DATA_DIR
    TEMPLATES_FOLDER = pathlib.Path(ROOT_DIR) / TEMPLATES_DIR
    GAMES_FOLDER = pathlib.Path(ROOT_DIR) / GAMES_DIR
    ASSETS_FOLDER = pathlib.Path(ROOT_DIR) / ASSETS_DIR
    LIVE_DATA_USED = False

    if LIVE_DATA_FOLDER.exists():
        LIVE_DATA_USED = True
        TEMPLATES_FOLDER_LIVE = pathlib.Path(LIVE_DATA_FOLDER) / TEMPLATES_DIR
        GAMES_FOLDER_LIVE = pathlib.Path(LIVE_DATA_FOLDER) / GAMES_DIR
        ASSETS_FOLDER_LIVE = pathlib.Path(LIVE_DATA_FOLDER) / ASSETS_DIR

    # Disable debug and reloader when using frozen data with live data - production mode
    if not LIVE_DATA_USED and FROZEN:
        DEBUG = False
        USE_RELOADER = False

#     check if exist TEMPLATES_DIR, STATIC_DIR, ASSETS_DIR
    if not TEMPLATES_FOLDER.exists():
        raise FileNotFoundError(f"Templates folder not found: {TEMPLATES_FOLDER}")

    if not GAMES_FOLDER.exists():
        raise FileNotFoundError(f"Games folder not found: {GAMES_FOLDER}")

    if not ASSETS_FOLDER.exists():
        raise FileNotFoundError(f"Assets folder not found: {ASSETS_FOLDER}")
