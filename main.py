# main.py
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QFrame, QWidget, QHBoxLayout, QPushButton, QLabel)
from PyQt5.QtGui import QSurfaceFormat, QFont, QColor
from PyQt5.QtCore import Qt, QPoint
from viewers.main_viewer import Viewer3D
from viewers.nav_controls import SideNavBar
from config.settings import APP_NAME, APP_COLOR_EXE, TOP_BT_NAV

class TitleBar(QWidget):
    """Barre de titre personnalisée avec boutons de contrôle"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(32)
        self.setStyleSheet(f"""
            TitleBar {{
                background-color: {APP_COLOR_EXE};
                border-bottom: 1px solid #2a4a6a;
            }}
            QLabel {{
                color: white;
                font-size: 12px;
                font-weight: bold;
                padding-left: 10px;
                background-color: {APP_COLOR_EXE};
            }}
            QPushButton {{
                background-color: {APP_COLOR_EXE};
                border: none;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 5px 10px;
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background-color: #2a5a8a;
            }}
            QPushButton#close:hover {{
                background-color: #e81123;
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Titre de la fenêtre
        self.title_label = QLabel(APP_NAME)
        self.title_label.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.title_label)
        
        # Espace flexible
        layout.addStretch()
        
        # Bouton minimiser
        self.btn_minimize = QPushButton("─")
        self.btn_minimize.setFixedSize(30, 32)
        self.btn_minimize.clicked.connect(self.parent.showMinimized)
        layout.addWidget(self.btn_minimize)
        
        # Bouton maximiser/restaurer
        self.btn_maximize = QPushButton("□")
        self.btn_maximize.setFixedSize(30, 32)
        self.btn_maximize.clicked.connect(self.toggle_maximize)
        layout.addWidget(self.btn_maximize)
        
        # Bouton fermer
        self.btn_close = QPushButton("✕")
        self.btn_close.setObjectName("close")
        self.btn_close.setFixedSize(30, 32)
        self.btn_close.clicked.connect(self.parent.close)
        layout.addWidget(self.btn_close)
        
        # Variables pour le déplacement de la fenêtre
        self.drag_pos = None
        self.setMouseTracking(True)
    
    def toggle_maximize(self):
        """Bascule entre maximisé et normal"""
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.btn_maximize.setText("□")
        else:
            self.parent.showMaximized()
            self.btn_maximize.setText("❐")
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos()
            self.parent.drag_start_pos = self.parent.pos()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if self.drag_pos is not None:
            delta = event.globalPos() - self.drag_pos
            self.parent.move(self.parent.drag_start_pos + delta)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        self.drag_pos = None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Enlever la décoration de la fenêtre
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
        
        # Barre de titre personnalisée
        self.title_bar = TitleBar(self)
        central_layout.addWidget(self.title_bar)
        
        # Viewer 3D
        self.viewer = Viewer3D()
        central_layout.addWidget(self.viewer)
        
        self.setCentralWidget(central_widget)
        
        # Barre de navigation latérale
        self.nav_bar = SideNavBar(self.viewer, self.viewer)
        
        self.setWindowTitle(APP_NAME)
        self.resize(1200, 800)
        
        # Variables pour le déplacement
        self.drag_start_pos = None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Positionner la barre de navigation latérale
        self.nav_bar.setGeometry(self.width() - 45, 100 + TOP_BT_NAV, 40, 270)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())