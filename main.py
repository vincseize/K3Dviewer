import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QSurfaceFormat, QColor, QFont
from PyQt5.QtCore import Qt

from viewers.main_viewer import Viewer3D, TOP_BT_NAV
from viewers.nav_bar import SideNavBar
from config.settings import *

class TitleBar(QWidget):
    """Barre de titre personnalisée intégrée au fichier main"""
    def __init__(self, parent, title=APP_NAME):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(32)
        self.setStyleSheet(f"""
            TitleBar {{ background-color: {APP_COLOR_EXE}; border-bottom: 1px solid #2a4a6a; }}
            QLabel {{ color: white; font-size: 12px; font-weight: bold; padding-left: 10px; }}
            QPushButton {{ background-color: {APP_COLOR_EXE}; border: none; color: white; font-size: 14px; padding: 5px 10px; }}
            QPushButton:hover {{ background-color: #2a5a8a; }}
            QPushButton#close:hover {{ background-color: #e81123; }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.title_label)
        layout.addStretch()
        
        btn_min = QPushButton("─")
        btn_min.clicked.connect(self.parent.showMinimized)
        layout.addWidget(btn_min)
        
        self.btn_max = QPushButton("□")
        self.btn_max.clicked.connect(self.toggle_maximize)
        layout.addWidget(self.btn_max)
        
        btn_close = QPushButton("✕")
        btn_close.setObjectName("close")
        btn_close.clicked.connect(self.parent.close)
        layout.addWidget(btn_close)

        self.start_pos = None

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.btn_max.setText("□")
        else:
            self.parent.showMaximized()
            self.btn_max.setText("❐")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.globalPos()
            self.window_pos = self.parent.pos()

    def mouseMoveEvent(self, event):
        if self.start_pos:
            delta = event.globalPos() - self.start_pos
            self.parent.move(self.window_pos + delta)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Fenêtre sans bordures
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(f"QMainWindow {{ background-color: {APP_COLOR_EXE}; }}")
        
        # Format OpenGL
        fmt = QSurfaceFormat()
        fmt.setSamples(8)
        QSurfaceFormat.setDefaultFormat(fmt)

        # Widget central et Layout principal
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Barre de titre
        self.title_bar = TitleBar(self, APP_NAME)
        layout.addWidget(self.title_bar)
        
        # Le Viewer 3D
        self.viewer = Viewer3D()
        layout.addWidget(self.viewer)
        self.setCentralWidget(central_widget)
        
        # La Barre de Navigation latérale (importée de nav_bar.py)
        # On l'attache au viewer pour qu'elle "flotte" dessus
        self.nav_bar = SideNavBar(self.viewer, self.viewer)
        
        self.resize(1200, 800)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Repositionnement de la navbar lors du redimensionnement
        if hasattr(self, 'nav_bar'):
            self.nav_bar.setGeometry(self.width() - 45, 100 + TOP_BT_NAV, 40, 280)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())