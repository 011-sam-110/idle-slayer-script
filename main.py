import json
import sys
import threading

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QLabel, QPushButton, QVBoxLayout,
                             QWidget)

from src import ChestHuntCheck, movement


def UpdateConfigSetting(settings: list):
    """Update a specific setting in the configuration file."""
    with open("src/config.json") as file:
        data = json.load(file)
    data[settings[0]] = settings[1] 
    with open("src/config.json", "w") as file:
        json.dump(data, file, indent=4)

def start():
    threading.Thread(target=movement.movementCycle).start()
    threading.Thread(target=ChestHuntCheck.ChestHuntCheck).start()
    # chest hunt check
    # trial check


class StartStopGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Start / Stop")
        self.setFixedSize(300, 150)

        self.running = False

        # UI elements
        self.status_label = QLabel("Status: Stopped")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")

        # Connect signals
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

    def start(self):
        if not self.running:
            self.running = True
            self.status_label.setText("Status: Running")
            UpdateConfigSetting(["paused", False])

    def stop(self):
        if self.running:
            self.running = False
            self.status_label.setText("Status: Stopped")
            UpdateConfigSetting(["paused", True])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartStopGUI()
    window.show()
    threading.Thread(target=start).start()
    sys.exit(app.exec_())
