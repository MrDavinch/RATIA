from PyQt5.QtWidgets import QApplication
from src.gui.splash_screen import SplashScreen
from src.gui.main_window import MonitorGrimaceApp
from PyQt5.QtCore import QTimer
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))


def main():
    app = QApplication(sys.argv)
    
    splash = SplashScreen()
    splash.show()
    QTimer.singleShot(2000, splash.close)

    window = MonitorGrimaceApp()
    QTimer.singleShot(2000, window.show)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()