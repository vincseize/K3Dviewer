# main.py
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QFrame, QWidget)
from PyQt5.QtGui import QSurfaceFormat, QFont, QColor
from PyQt5.QtCore import Qt
from viewers.main_viewer import Viewer3D
from viewers.nav_controls import SideNavBar
from config.settings import APP_NAME, APP_COLOR_EXE, TOP_BT_NAV

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        fmt = QSurfaceFormat()
        fmt.setSamples(8)
        QSurfaceFormat.setDefaultFormat(fmt)
        
        # Widget central
        central_widget = QWidget()
        central_widget.setStyleSheet(f"background-color: {APP_COLOR_EXE};")
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)
        
        # Viewer 3D
        self.viewer = Viewer3D()
        central_layout.addWidget(self.viewer)
        
        self.setCentralWidget(central_widget)
        
        # Barre de navigation latérale
        self.nav_bar = SideNavBar(self.viewer, self.viewer)
        self.nav_bar.setGeometry(self.width() - 45, 100 + TOP_BT_NAV, 40, 270)
        
        self.setWindowTitle(APP_NAME)
        self.resize(1200, 800)
        self.start_pos = None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.nav_bar.setGeometry(self.width() - 45, 100 + TOP_BT_NAV, 40, 270)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())