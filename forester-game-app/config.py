import os
import sys
from app.utils import get_local_ip_address


class Config:
    DATAFILE = "data.json"
    LOG_FOLDER = "ForesterLogs"
    ALLOWED_EXTENSIONS = ["json"]
    IP_ADDRESS = get_local_ip_address()
    VERSION = "1.1.0"

    if getattr(sys, "frozen", False):
        # frozen
        ROOT_DIR = os.path.dirname(sys.executable)
        TEMP_DIR = sys._MEIPASS
        TEMPLATES_DIR = os.path.join(sys._MEIPASS, "templates")
        STATIC_DIR = os.path.join(sys._MEIPASS, "static")
        PORT = 80
        DEBUG = False
        USE_RELOADER = False
    else:
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        TEMP_DIR = "-"
        TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")
        STATIC_DIR = os.path.join(ROOT_DIR, "static")
        PORT = 4444
        DEBUG = True
        USE_RELOADER = True
