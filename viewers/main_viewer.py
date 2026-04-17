# viewers/main_viewer.py
import numpy as np
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QPixmap, QPainter, QPen, QColor
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from utils.logger import debug_log

from .viewer_core import ViewerCore
from .viewer_navigation import ViewerNavigation
from .viewer_rendering import ViewerRendering
from .gizmo import Gizmo
from menus.context_menu import MainContextMenu

class Viewer3D(ViewerCore, ViewerNavigation, ViewerRendering):
    def __init__(self, parent=None):
        self.debug = False
        super().__init__(parent)
        self.setup_nav_states()
        self.context_menu = MainContextMenu(self)
        self.zoom_cursor = self._create_nav_cursor("zoom")
        self.pan_cursor = self._create_nav_cursor("pan")
        

    def initializeGL(self):
        glutInit()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        from config.settings import C_BG
        glClearColor(*C_BG)
        self.update_projection()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(self.pan_x, self.pan_y, self.zoom)
        glRotatef(self.rot_x, 1, 0, 0)
        glRotatef(self.rot_y, 0, 1, 0)
        mv_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        if self.show_grid: 
            self.draw_grid()
        self.draw_cube_centered()
        if self.show_axes: 
            self.draw_world_axes()
        glDisable(GL_DEPTH_TEST)
        Gizmo.render(self.width(), self.height(), mv_matrix)
        glEnable(GL_DEPTH_TEST)

    def activate_zoom_mode(self, checked):
        self.zoom_mode = checked
        # Désactiver le pan quand on active le zoom
        if checked:
            self.pan_mode = False
            self.is_panning = False
            self.setCursor(self.zoom_cursor)
            debug_log("MainViewer", "Mode Zoom ACTIVÉ - Pan désactivé", self.debug)
        else:
            self.unsetCursor()
            debug_log("MainViewer", "Mode Zoom DÉSACTIVÉ", self.debug)

    def activate_pan_mode(self, checked):
        self.pan_mode = checked
        # Désactiver le zoom quand on active le pan
        if checked:
            self.zoom_mode = False
            self.is_zooming = False
            self.setCursor(self.pan_cursor)
            debug_log("MainViewer", "Mode Pan ACTIVÉ - Zoom désactivé", self.debug)
        else:
            self.unsetCursor()
            debug_log("MainViewer", "Mode Pan DÉSACTIVÉ", self.debug)

    def _sync_navbar_ui(self):
        root = self.window()
        if hasattr(root, 'nav_bar'):
            root.nav_bar.uncheck_all_modes()

    def wheelEvent(self, event):
        self.handle_wheel_zoom(event.angleDelta().y())
        self.update_projection()
        self.update()

    def mousePressEvent(self, event):
        self.last_pos = event.pos()
        
        # Mode Pan actif ET clic gauche (PAN)
        if self.pan_mode and event.button() == Qt.LeftButton: 
            self.is_panning = True
            debug_log("MainViewer", "Pan drag démarré")
        # Mode Zoom actif ET clic gauche (ZOOM)
        elif self.zoom_mode and event.button() == Qt.LeftButton: 
            self.is_zooming = True
            debug_log("MainViewer", "Zoom drag démarré")
        elif event.button() == Qt.RightButton:
            self.context_menu.exec_(event.globalPos())
        elif event.button() == Qt.MidButton:
            if not self.pan_mode and not self.zoom_mode:
                self._sync_navbar_ui()

    def mouseMoveEvent(self, event):
        diff = event.pos() - self.last_pos
        
        # PAN en mode drag
        if self.pan_mode and self.is_panning:
            self.compute_pan(diff.x(), diff.y())
            debug_log("MainViewer", f"Pan: dx={diff.x()}, dy={diff.y()}")
        # ZOOM en mode drag
        elif self.zoom_mode and self.is_zooming:
            from config.settings import ZOOM_SPEED
            self.zoom = np.clip(self.zoom + diff.y() * ZOOM_SPEED, -30.0, -2.0)
            self.update_projection()
            debug_log("MainViewer", f"Zoom: {self.zoom}")
        # Clic milieu : rotation ou pan avec Shift
        elif event.buttons() & Qt.MidButton:
            if QApplication.keyboardModifiers() & Qt.ShiftModifier:
                self.compute_pan(diff.x(), diff.y())
            else:
                self.compute_rotation(diff.x(), diff.y())
        
        self.last_pos = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.is_zooming = False
        self.is_panning = False

    def resizeGL(self, w, h):
        self.update_projection()