import os
import sys


class Config:
    DATAFILE = 'data.json'
    ALLOWED_EXTENSIONS = ['json']

    if getattr(sys, 'frozen', False):
        # frozen
        ROOT_DIR = os.path.dirname(sys.executable)
        TEMPLATES_DIR = os.path.join(sys._MEIPASS, 'templates')
        STATIC_DIR = os.path.join(sys._MEIPASS, 'static')
        DEBUG = False
    else:
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        TEMPLATES_DIR = os.path.join(ROOT_DIR, 'templates')
        STATIC_DIR = os.path.join(ROOT_DIR, 'static')
        DEBUG = True
