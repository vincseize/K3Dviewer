# viewers/viewer_core.py
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import Qt, QPoint
from config.settings import TOP_BT_NAV
from utils.logger import debug_log

# TOP_BT_NAV = 50

class ViewerCore(QOpenGLWidget):
    def __init__(self, parent=None):
        
        super().__init__(parent)
        self.def_zoom = -12.0
        self.zoom = self.def_zoom
        self.pan_x, self.pan_y = 0.0, 0.0
        self.rot_x, self.rot_y = 25.0, -45.0
        self.is_ortho = False
        self.show_grid = True
        self.show_axes = True
        self.last_pos = QPoint()
        self.setFocusPolicy(Qt.StrongFocus)
        self.debug = False
        

    def set_projection(self, ortho_mode):
        debug_log("ViewerCore", f"set_projection reçu: {ortho_mode}", self.debug)
        self.is_ortho = ortho_mode
        self.makeCurrent()
        self.update_projection()
        self.update()

    def set_grid_visible(self, visible):
        self.show_grid = visible
        self.update()

    def set_axes_visible(self, visible):
        self.show_axes = visible
        self.update()

    def reset_view(self):
        self.zoom = self.def_zoom
        self.pan_x, self.pan_y = 0.0, 0.0
        self.rot_x, self.rot_y = 25.0, -45.0
        self.update_projection()
        self.update()