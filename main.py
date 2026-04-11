# main.py
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QFrame, QPushButton, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QSurfaceFormat, QIcon, QPixmap, QPainter, QCursor
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import Qt, QSize
from viewers.main_viewer import Viewer3D, TOP_BT_NAV
from config.settings import *
from menus.svg_icons import SVG_ICONS

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

        # Bouton Zoom (Toggle avec icône)
        self.btn_zoom = NavButton("zoom", "Mode Zoom (Activer/Désactiver)", True, False)
        self.btn_zoom.setCheckable(True)
        self.btn_zoom.setChecked(False)
        
        # Bouton Pan (pas de fonction pour le moment)
        self.btn_pan = NavButton("pan", "Pan (à venir)", False)
        
        # Espace équivalent à la hauteur d'un bouton (30px) + espacement (8px)
        spacer = QSpacerItem(20, 38, QSizePolicy.Minimum, QSizePolicy.Fixed)
        
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
        layout.addWidget(self.btn_zoom)
        layout.addWidget(self.btn_pan)
        layout.addItem(spacer)
        layout.addWidget(self.btn_proj)
        layout.addWidget(self.btn_home)
        layout.addWidget(self.btn_grid)
        layout.addWidget(self.btn_axes)

        # Connexions
        self.btn_zoom.toggled.connect(self.toggle_zoom_mode)
        self.btn_proj.toggled.connect(self.toggle_projection)
        self.btn_home.clicked.connect(self.viewer.reset_view)
        self.btn_grid.toggled.connect(self.toggle_grid)
        self.btn_axes.toggled.connect(self.toggle_axes)

    def toggle_zoom_mode(self, checked):
        """Active/désactive le mode zoom."""
        if checked:
            self.viewer.activate_zoom_mode()
        else:
            self.viewer.deactivate_zoom_mode()

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

    def toggle_axes(self, checked):
        """Affiche/masque les axes."""
        self.viewer.set_axes_visible(checked)
        self.btn_axes.update_icon()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Positionnement dynamique sous le Gizmo (6 boutons + espace)
        self.nav_frame.setGeometry(self.width() - 45, 100 + TOP_BT_NAV, 40, 230)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())