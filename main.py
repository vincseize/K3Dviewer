# main.py
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QFrame, QPushButton, QButtonGroup)
from PyQt5.QtGui import QSurfaceFormat, QIcon, QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import Qt, QSize
from viewers.main_viewer import Viewer3D, TOP_BT_NAV
from config.settings import *

SVG_ICONS = {
    "persp": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#ddd" stroke-width="2"/></svg>""",
    "ortho": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 3H21V21H3V3Z" stroke="#ddd" stroke-width="2"/><path d="M12 3V21M3 12H21" stroke="#ddd" stroke-opacity="0.3"/></svg>""",
    "hand": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M18 11V6a2 2 0 00-4 0v5m0 0V5a2 2 0 00-4 0v6m0 0V6a2 2 0 00-4 0v9a7 7 0 007 7h2a7 7 0 007-7v-4a2 2 0 00-4 0z" stroke="#ddd" stroke-width="2"/></svg>""",
    "zoom": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="11" cy="11" r="8" stroke="#ddd" stroke-width="2"/><path d="M21 21l-4.35-4.35" stroke="#ddd" stroke-width="2"/></svg>""",
    "home": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 9L12 2L21 9V20a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" stroke="#ddd" stroke-width="2"/><path d="M9 22V12h6v10" stroke="#ddd" stroke-width="2"/></svg>""",
    "grid": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 3h7v7H3V3zm11 0h7v7h-7V3zm0 11h7v7h-7v-7zM3 14h7v7H3v-7z" stroke="#ddd" stroke-width="2"/></svg>"""
}

class NavButton(QPushButton):
    def __init__(self, icon_key, tip, checkable=True):
        super().__init__()
        self.setFixedSize(30, 30)
        self.setToolTip(tip)
        self.setCheckable(checkable)
        
        renderer = QSvgRenderer(SVG_ICONS[icon_key].encode())
        pix = QPixmap(30, 30)
        pix.fill(Qt.transparent)
        painter = QPainter(pix)
        renderer.render(painter)
        painter.end()
        self.setIcon(QIcon(pix))
        self.setIconSize(QSize(16, 16))
        self.setStyleSheet("""
            QPushButton { background: rgba(40,40,40,220); border: 1px solid #444; border-radius: 15px; }
            QPushButton:hover { background: #444; border-color: #0078d7; }
            QPushButton:checked { background: #0078d7; border-color: white; }
        """)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        fmt = QSurfaceFormat()
        fmt.setSamples(8)
        QSurfaceFormat.setDefaultFormat(fmt)
        
        self.viewer = Viewer3D()
        self.setCentralWidget(self.viewer)
        
        self.init_nav_bar()
        self.setWindowTitle(APP_NAME)
        self.resize(1200, 800)

    def init_nav_bar(self):
        # Frame flottante verticale
        self.nav_frame = QFrame(self.viewer)
        layout = QVBoxLayout(self.nav_frame)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)

        # Bouton unique Perspective/Ortho (Toggle)
        self.btn_proj = NavButton("persp", "Mode Perspective (cliquer pour Orthographique)")
        self.btn_proj.setCheckable(True)
        self.btn_proj.setChecked(False)  # Perspective par défaut
        
        # Autres boutons
        self.btn_home = NavButton("home", "Reset Camera", False)
        self.btn_grid = NavButton("grid", "Toggle Grid")
        
        # On ajoute au layout
        layout.addWidget(self.btn_proj)
        layout.addWidget(self.btn_home)
        layout.addWidget(self.btn_grid)

        # Setup initial
        self.btn_grid.setChecked(True)

        # Connexions
        self.btn_proj.toggled.connect(self.toggle_projection)
        self.btn_home.clicked.connect(self.viewer.reset_view)
        self.btn_grid.toggled.connect(self.viewer.set_grid_visible)
        
        # Mise à jour initiale de l'icône
        self.update_proj_icon()

    def toggle_projection(self, checked):
        """Bascule entre Perspective (False) et Orthographique (True)."""
        # checked = True -> Ortho, False -> Perspective
        self.viewer.set_projection(checked)
        self.update_proj_icon()
    
    def update_proj_icon(self):
        """Met à jour l'icône du bouton selon le mode actuel."""
        if self.viewer.is_ortho:
            # Mode Orthographique actif
            renderer = QSvgRenderer(SVG_ICONS["ortho"].encode())
            self.btn_proj.setToolTip("Mode Orthographique (cliquer pour Perspective)")
        else:
            # Mode Perspective actif
            renderer = QSvgRenderer(SVG_ICONS["persp"].encode())
            self.btn_proj.setToolTip("Mode Perspective (cliquer pour Orthographique)")
        
        # Mise à jour de l'icône
        pix = QPixmap(30, 30)
        pix.fill(Qt.transparent)
        painter = QPainter(pix)
        renderer.render(painter)
        painter.end()
        self.btn_proj.setIcon(QIcon(pix))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Positionnement dynamique sous le Gizmo (Top-Right)
        # Utilisation de TOP_BT_NAV pour le décalage vertical
        self.nav_frame.setGeometry(self.width() - 45, 100 + TOP_BT_NAV, 40, 120)  # Hauteur réduite (3 boutons au lieu de 4)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())