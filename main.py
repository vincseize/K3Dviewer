# main.py
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QFrame, QPushButton)
from PyQt5.QtGui import QSurfaceFormat, QIcon, QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import Qt, QSize
from viewers.main_viewer import Viewer3D, TOP_BT_NAV
from config.settings import *

SVG_ICONS = {
    "persp": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#ddd" stroke-width="2"/></svg>""",
    "ortho": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 3H21V21H3V3Z" stroke="#ddd" stroke-width="2"/><path d="M12 3V21M3 12H21" stroke="#ddd" stroke-opacity="0.3"/></svg>""",
    "home": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 9L12 2L21 9V20a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" stroke="#ddd" stroke-width="2"/><path d="M9 22V12h6v10" stroke="#ddd" stroke-width="2"/></svg>""",
    "grid": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 3h7v7H3V3zm11 0h7v7h-7V3zm0 11h7v7h-7v-7zM3 14h7v7H3v-7z" stroke="#ddd" stroke-width="2"/></svg>""",
    "axes_on": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><line x1="3" y1="12" x2="21" y2="12" stroke="#f00" stroke-width="2"/><line x1="12" y1="3" x2="12" y2="21" stroke="#0f0" stroke-width="2"/><circle cx="12" cy="12" r="2" fill="#00f"/></svg>""",
    "axes_off": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><line x1="3" y1="12" x2="21" y2="12" stroke="#f00" stroke-width="2" stroke-opacity="0.3"/><line x1="12" y1="3" x2="12" y2="21" stroke="#0f0" stroke-width="2" stroke-opacity="0.3"/><circle cx="12" cy="12" r="2" fill="#00f" fill-opacity="0.3"/><line x1="3" y1="21" x2="21" y2="3" stroke="#d00" stroke-width="2"/></svg>"""
}

class NavButton(QPushButton):
    def __init__(self, icon_key, tip, checkable=True, has_toggle_icon=False, icon_key_off=None):
        super().__init__()
        self.icon_key = icon_key
        self.icon_key_off = icon_key_off
        self.has_toggle_icon = has_toggle_icon
        self.setFixedSize(30, 30)
        self.setToolTip(tip)
        self.setCheckable(checkable)
        self.setStyleSheet("""
            QPushButton { background: rgba(40,40,40,220); border: 1px solid #444; border-radius: 15px; }
            QPushButton:hover { background: #444; border-color: #0078d7; }
            QPushButton:checked { background: #0078d7; border-color: white; }
        """)
        self.update_icon()
    
    def update_icon(self):
        """Met à jour l'icône selon l'état checked."""
        if self.has_toggle_icon and self.isChecked():
            icon_key = self.icon_key_off
        else:
            icon_key = self.icon_key
        
        renderer = QSvgRenderer(SVG_ICONS[icon_key].encode())
        pix = QPixmap(30, 30)
        pix.fill(Qt.transparent)
        painter = QPainter(pix)
        renderer.render(painter)
        painter.end()
        self.setIcon(QIcon(pix))
        self.setIconSize(QSize(16, 16))

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

        # Bouton Perspective/Ortho (Toggle avec 2 icônes)
        self.btn_proj = NavButton("persp", "Mode Perspective", True, True, "ortho")
        self.btn_proj.setChecked(False)
        
        # Bouton Home (sans toggle)
        self.btn_home = NavButton("home", "Reset Camera", False)
        
        # Bouton Grid (Toggle MAIS sans changement d'icône)
        self.btn_grid = NavButton("grid", "Afficher/Masquer la grille", True, False)
        self.btn_grid.setChecked(True)
        
        # Bouton Axes (Toggle avec 2 icônes)
        self.btn_axes = NavButton("axes_on", "Afficher/Masquer les axes", True, True, "axes_off")
        self.btn_axes.setChecked(True)
        
        # On ajoute au layout
        layout.addWidget(self.btn_proj)
        layout.addWidget(self.btn_home)
        layout.addWidget(self.btn_grid)
        layout.addWidget(self.btn_axes)

        # Connexions
        self.btn_proj.toggled.connect(self.toggle_projection)
        self.btn_home.clicked.connect(self.viewer.reset_view)
        self.btn_grid.toggled.connect(self.toggle_grid)
        self.btn_axes.toggled.connect(self.toggle_axes)

    def toggle_projection(self, checked):
        """Bascule entre Perspective (False) et Orthographique (True)."""
        self.viewer.set_projection(checked)
        self.btn_proj.update_icon()
        if checked:
            self.btn_proj.setToolTip("Mode Orthographique (cliquer pour Perspective)")
        else:
            self.btn_proj.setToolTip("Mode Perspective (cliquer pour Orthographique)")

    def toggle_grid(self, checked):
        """Affiche/masque la grille."""
        self.viewer.set_grid_visible(checked)
        # Pas de mise à jour d'icône pour grid

    def toggle_axes(self, checked):
        """Affiche/masque les axes."""
        self.viewer.set_axes_visible(checked)
        self.btn_axes.update_icon()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Positionnement dynamique sous le Gizmo (4 boutons)
        self.nav_frame.setGeometry(self.width() - 45, 100 + TOP_BT_NAV, 40, 155)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())