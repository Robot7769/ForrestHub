import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit
from .ws_lib import WebSocketServer

class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)
        self.setLayout(self.layout)

        self.websocket_thread = WebSocketServer()
        self.websocket_thread.messageReceived.connect(self.update_text)
        self.websocket_thread.start()

    def update_text(self, message):
        self.text_edit.append(message)
