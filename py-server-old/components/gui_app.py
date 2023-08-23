import json
import sys

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTextEdit,
                             QPushButton, QHBoxLayout, QLabel, QSpinBox,
                             QTreeWidget, QTreeWidgetItem, QMessageBox)

from .database import save_data
from .ws_lib import WebSocketServer
from .timer_widget import TimerWidget
from .database import load_data, save_data

class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Main Layout
        self.layout = QVBoxLayout()

        # Timer Configurator
        self.timer_widget = TimerWidget()
        self.layout.addWidget(self.timer_widget)
        self.timer_widget.timeChanged.connect(self.handle_time_change)

        # Data Display
        self.data_tree = QTreeWidget(self)
        self.data_tree.setHeaderLabels(["Key", "Value"])
        self.data_tree.itemDoubleClicked.connect(self.edit_item)

        self.layout.addWidget(self.data_tree)
        self.setLayout(self.layout)

        self.websocket_thread = WebSocketServer()
        self.websocket_thread.messageReceived.connect(self.update_data)
        self.websocket_thread.start()

    def load_tree_data(self):
        store_data = load_data()  # Load data from the database
        self.update_data(store_data)

    def update_data(self, store_data):
        self.data_tree.clear()
        for key, value in store_data.items():
            item = QTreeWidgetItem(self.data_tree)
            item.setText(0, key)
            item.setText(1, str(value))
            item.setFlags(item.flags() | Qt.ItemIsEditable)  # make the item editable

    def handle_time_change(self, time: str):
        # Here, format the data as required to send over WebSocket
        data = {
            'action': 'update_time',
            'payload': time
        }
        self.websocket_thread.send_data(data)

    def edit_item(self, item, column):
        self.data_tree.editItem(item, column)

        # Save the edited data back to the database
        store_data = {}
        for index in range(self.data_tree.topLevelItemCount()):
            item = self.data_tree.topLevelItem(index)
            key = item.text(0)
            value = item.text(1)
            store_data[key] = value
        save_data(store_data)

    def remove_selected_item(self):
        selected_items = self.data_tree.selectedItems()
        for item in selected_items:
            index = self.data_tree.indexOfTopLevelItem(item)
            self.data_tree.takeTopLevelItem(index)

        # Save the updated data back to the database after deletion
        store_data = {}
        for index in range(self.data_tree.topLevelItemCount()):
            item = self.data_tree.topLevelItem(index)
            key = item.text(0)
            value = item.text(1)
            store_data[key] = value
        save_data(store_data)

    def closeEvent(self, event: QEvent):
        """
        This method is automatically called when the window is closed.
        """
        # Prompt user to confirm closure
        reply = QMessageBox.question(self, 'Confirm Exit',
                                     'Are you sure you want to close the application?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Close WebSocket thread
            self.websocket_thread.terminate()
            event.accept()  # Confirm the close event
        else:
            event.ignore()  # Ignore the close event