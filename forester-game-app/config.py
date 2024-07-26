import os
import sys
from app.utils import get_local_ip_address


class Config:
    DATAFILE = "data.json"
    ALLOWED_EXTENSIONS = ["json"]
    PORT = 5000
    IP_ADDRESS = get_local_ip_address()

    if getattr(sys, "frozen", False):
        # frozen
        ROOT_DIR = os.path.dirname(sys.executable)
        TEMPLATES_DIR = os.path.join(sys._MEIPASS, "templates")
        STATIC_DIR = os.path.join(sys._MEIPASS, "static")
        DEBUG = False
        # use_reloader
        USE_RELOADER = False
    else:
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")
        STATIC_DIR = os.path.join(ROOT_DIR, "static")
        DEBUG = True
        USE_RELOADER = True
