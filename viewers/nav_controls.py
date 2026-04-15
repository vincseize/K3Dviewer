# viewers/nav_controls.py
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import Qt, QSize
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
        self.toggled.connect(self.update_icon)
    
    def update_icon(self):
        key = self.icon_key_off if (self.has_toggle_icon and self.isChecked()) else self.icon_key
        if key not in SVG_ICONS: 
            return
        renderer = QSvgRenderer(SVG_ICONS[key].encode())
        pix = QPixmap(30, 30)
        pix.fill(Qt.transparent)
        painter = QPainter(pix)
        renderer.render(painter)
        painter.end()
        self.setIcon(QIcon(pix))
        self.setIconSize(QSize(16, 16))

class SideNavBar(QFrame):
    def __init__(self, parent, viewer):
        super().__init__(parent)
        self.viewer = viewer
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)

        self.btn_zoom = NavButton("zoom", "Mode Zoom", True)
        self.btn_pan = NavButton("pan", "Mode Pan", True)
        self.btn_proj = NavButton("persp", "Perspective/Ortho", True, True, "ortho")
        self.btn_home = NavButton("home", "Reset View", False)
        self.btn_grid = NavButton("grid", "Grille", True)
        self.btn_grid.setChecked(True)
        self.btn_axes = NavButton("axes_on", "Axes", True, True, "axes_off")
        self.btn_axes.setChecked(True)

        layout.addWidget(self.btn_zoom)
        layout.addWidget(self.btn_pan)
        layout.addSpacing(15) 
        layout.addWidget(self.btn_proj)
        layout.addWidget(self.btn_home)
        layout.addWidget(self.btn_grid)
        layout.addWidget(self.btn_axes)

        self.btn_zoom.toggled.connect(self._toggle_zoom)
        self.btn_pan.toggled.connect(self._toggle_pan)
        self.btn_proj.toggled.connect(self.viewer.set_projection)
        self.btn_home.clicked.connect(self.viewer.reset_view)
        self.btn_grid.toggled.connect(self.viewer.set_grid_visible)
        self.btn_axes.toggled.connect(self.viewer.set_axes_visible)

    def _toggle_zoom(self, checked):
        if checked:
            self.btn_pan.blockSignals(True)
            self.btn_pan.setChecked(False)
            self.btn_pan.blockSignals(False)
            self.viewer.activate_zoom_mode(True)
        else:
            self.viewer.activate_zoom_mode(False)

    def _toggle_pan(self, checked):
        if checked:
            self.btn_zoom.blockSignals(True)
            self.btn_zoom.setChecked(False)
            self.btn_zoom.blockSignals(False)
            self.viewer.activate_pan_mode(True)
        else:
            self.viewer.activate_pan_mode(False)

    def uncheck_all_modes(self):
        self.btn_zoom.blockSignals(True)
        self.btn_pan.blockSignals(True)
        self.btn_zoom.setChecked(False)
        self.btn_pan.setChecked(False)
        self.btn_zoom.blockSignals(False)
        self.btn_pan.blockSignals(False)