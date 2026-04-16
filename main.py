# main.py
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QWidget, QHBoxLayout, QPushButton, QLabel)
from PyQt5.QtGui import QSurfaceFormat, QFont, QIcon, QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import Qt
from viewers.main_viewer import Viewer3D
from viewers.nav_controls import SideNavBar
from menus.menu_bar import MenuBarManager
from config.settings import APP_NAME, APP_COLOR_EXE, TOP_BT_NAV
from menus.svg_icons import SVG_ICONS

def load_stylesheet(filename):
    """Charge un fichier QSS et remplace les variables"""
    with open(filename, 'r') as f:
        stylesheet = f.read()
    stylesheet = stylesheet.replace('#204060', APP_COLOR_EXE)
    return stylesheet

def create_app_icon(size=64):
    """Crée l'icône de l'application à partir du SVG"""
    renderer = QSvgRenderer(SVG_ICONS["favicon"].encode())
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap), pixmap

class TitleBar(QWidget):
    """Barre de titre personnalisée avec boutons de contrôle"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(32)
        self.setStyleSheet(load_stylesheet('stylesheets/menuBar-stylesheet.qss'))
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 0, 0)
        layout.setSpacing(0)
        
        # Icône
        _, icon_pixmap = create_app_icon(64)
        self.icon_label = QLabel()
        scaled_icon = icon_pixmap.scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(scaled_icon)
        self.icon_label.setFixedSize(24, 32)
        self.icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.icon_label)
        
        # Titre
        layout.addSpacing(5)
        self.title_label = QLabel(APP_NAME)
        self.title_label.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.title_label)
        
        layout.addStretch()
        
        # Boutons de contrôle
        for btn_text, func, name in [
            ("─", self.parent.showMinimized, "min"),
            ("□", self.toggle_maximize, "max"),
            ("✕", self.parent.close, "close")
        ]:
            btn = QPushButton(btn_text)
            btn.setFixedSize(45, 32)
            if name == "close": 
                btn.setObjectName("close")
            btn.clicked.connect(func)
            if btn_text == "□": 
                self.btn_maximize = btn
            layout.addWidget(btn)

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
        
        # Barre de titre
        self.title_bar = TitleBar(self)
        central_layout.addWidget(self.title_bar)
        
        # Viewer 3D
        self.viewer = Viewer3D()
        
        # Barre de menu
        self.menu_manager = MenuBarManager(self, self.viewer)
        menu_bar = self.menu_manager.setup_menu_bar()
        menu_bar.setFixedHeight(28)
        central_layout.addWidget(menu_bar)
        
        # Viewer
        central_layout.addWidget(self.viewer)
        
        self.setCentralWidget(central_widget)
        
        # Barre de navigation latérale
        self.nav_bar = SideNavBar(self.viewer, self.viewer)
        
        self.setWindowTitle(APP_NAME)
        self.resize(1200, 800)
        
        # Icône de la fenêtre
        app_icon, _ = create_app_icon(64)
        self.setWindowIcon(app_icon)
        
        self.drag_start_pos = None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.nav_bar.setGeometry(self.width() - 45, 60 + TOP_BT_NAV, 40, 270)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())