from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import Qt, QSize
from menus.svg_icons import SVG_ICONS

class NavButton(QPushButton):
    """Bouton stylisé avec support SVG et toggle d'icônes"""
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
        self.toggled.connect(self.update_icon)
    
    def update_icon(self):
        """Met à jour l'icône selon l'état du bouton."""
        key = self.icon_key_off if (self.has_toggle_icon and self.isChecked()) else self.icon_key
        
        renderer = QSvgRenderer(SVG_ICONS[key].encode())
        pix = QPixmap(30, 30)
        pix.fill(Qt.transparent)
        painter = QPainter(pix)
        renderer.render(painter)
        painter.end()
        self.setIcon(QIcon(pix))
        self.setIconSize(QSize(16, 16))