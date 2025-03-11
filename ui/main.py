from PyQt6.QtWidgets import QApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtCore import QUrl
import os

import sys

app = QApplication(sys.argv)
engine = QQmlApplicationEngine()

qml_file = os.path.join(os.path.dirname(__file__), "Main.qml")
engine.load(os.path.abspath(qml_file))

sys.exit(app.exec())
