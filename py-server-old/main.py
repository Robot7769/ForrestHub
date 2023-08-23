import sys
import webbrowser
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from threading import Thread

from components.gui_app import SimpleApp
from components.flask_app import run_flask_app


if __name__ == '__main__':
    t = Thread(target=run_flask_app)
    t.start()
    QTimer.singleShot(1000, lambda: webbrowser.open("http://127.0.0.1:5000"))
    qt_app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    sys.exit(qt_app.exec_())
