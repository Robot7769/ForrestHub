import sys
import asyncio
import websockets
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpinBox, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt, pyqtSignal

class TimerWidget(QWidget):
    timeChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.remaining_seconds = 0

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Time Configurator
        self.timer_layout = QHBoxLayout()
        self.hours_spin = QSpinBox(self)
        self.hours_spin.setMaximum(23)
        self.minutes_spin = QSpinBox(self)
        self.minutes_spin.setMaximum(59)
        self.seconds_spin = QSpinBox(self)
        self.seconds_spin.setMaximum(59)

        self.timer_layout.addWidget(self.hours_spin)
        self.timer_layout.addWidget(QLabel("H"))
        self.timer_layout.addWidget(self.minutes_spin)
        self.timer_layout.addWidget(QLabel("M"))
        self.timer_layout.addWidget(self.seconds_spin)
        self.timer_layout.addWidget(QLabel("S"))

        # Buttons
        self.start_btn = QPushButton('Start', self)
        self.start_btn.clicked.connect(self.start_timer)
        self.pause_btn = QPushButton('Pause', self)
        self.pause_btn.clicked.connect(self.pause_timer)
        self.end_btn = QPushButton('End Game', self)
        self.end_btn.clicked.connect(self.end_timer)

        self.timer_layout.addWidget(self.start_btn)
        self.timer_layout.addWidget(self.pause_btn)
        self.timer_layout.addWidget(self.end_btn)

        self.layout.addLayout(self.timer_layout)
        self.setLayout(self.layout)

        # QTimer for the countdown
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

    def start_timer(self):
        hours = self.hours_spin.value()
        minutes = self.minutes_spin.value()
        seconds = self.seconds_spin.value()

        self.remaining_seconds = hours * 3600 + minutes * 60 + seconds

        self.hours_spin.setEnabled(False)
        self.minutes_spin.setEnabled(False)
        self.seconds_spin.setEnabled(False)

        if self.remaining_seconds <= 0:
            self.timeChanged.emit("Hra běží")
            return

        if not self.timer.isActive():
            self.timer.start(1000)

    def pause_timer(self):
        self.timeChanged.emit("Zastaveno")
        if self.timer.isActive():
            self.timer.stop()


    def end_timer(self):
        self.timer.stop()
        self.remaining_seconds = 0
        self.update_time_display()
        self.timeChanged.emit("Konec hry")

        self.hours_spin.setEnabled(True)
        self.minutes_spin.setEnabled(True)
        self.seconds_spin.setEnabled(True)

    def update_timer(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_time_display()
            self.send_time_data()  # Send the remaining time via WebSocket

            if self.remaining_seconds == 0:
                self.timer.stop()
        else:
            self.timer.stop()
            self.end_timer()

    def update_time_display(self):
        hours = self.remaining_seconds // 3600
        minutes = (self.remaining_seconds % 3600) // 60
        seconds = self.remaining_seconds % 60

        self.hours_spin.setValue(hours)
        self.minutes_spin.setValue(minutes)
        self.seconds_spin.setValue(seconds)

        formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
        self.timeChanged.emit(formatted_time)

    def send_time_data(self):
        data = {"action": "update_time", "time": self.remaining_seconds}
        # Implement WebSocket logic here to send the data
