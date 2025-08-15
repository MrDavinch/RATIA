# Pantalla de carga

from PyQt5.QtWidgets import QSplashScreen
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__(QPixmap("resources/logo.jpeg").scaled(400, 300, Qt.KeepAspectRatio))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)