# viewers/main_viewer.py
import numpy as np
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QPixmap, QPainter, QPen, QColor
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from .viewer_core import ViewerCore
from .viewer_navigation import ViewerNavigation
from .viewer_rendering import ViewerRendering
from .gizmo import Gizmo
from .menu_bar import MenuBar
from menus.context_menu import MainContextMenu

class Viewer3D(ViewerCore, ViewerNavigation, ViewerRendering):
    def __init__(self, parent=None):
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
        cursor_pos = self.mapFromGlobal(QCursor.pos())
        MenuBar.render(self.width(), self.height(), cursor_pos.x(), self.height() - cursor_pos.y())
        glEnable(GL_DEPTH_TEST)

    def activate_zoom_mode(self, checked):
        self.zoom_mode = checked
        if checked: 
            self.setCursor(self.zoom_cursor)
        else: 
            self.unsetCursor()

    def activate_pan_mode(self, checked):
        self.pan_mode = checked
        if checked: 
            self.setCursor(self.pan_cursor)
        else: 
            self.unsetCursor()

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
        if MenuBar.handle_click(event.x(), self.height(), self.height()):
            self.update()
            return
        
        if self.pan_mode and event.button() == Qt.LeftButton: 
            self.is_panning = True
        elif self.zoom_mode and event.button() == Qt.LeftButton: 
            self.is_zooming = True
        elif event.button() == Qt.RightButton:
            self.context_menu.exec_(event.globalPos())
        elif event.button() == Qt.MidButton:
            if not self.pan_mode and not self.zoom_mode:
                self._sync_navbar_ui()

    def mouseMoveEvent(self, event):
        diff = event.pos() - self.last_pos
        if self.pan_mode and self.is_panning: 
            self.compute_pan(diff.x(), diff.y())
        elif self.zoom_mode and self.is_zooming:
            self.zoom = np.clip(self.zoom + diff.y() * 0.05, -30.0, -2.0)
            self.update_projection()
        elif event.buttons() & Qt.MidButton:
            if QApplication.keyboardModifiers() & Qt.ShiftModifier:
                self.compute_pan(diff.x(), diff.y())
            else:
                self.compute_rotation(diff.x(), diff.y())
        self.last_pos = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.is_panning = False
        self.is_zooming = False

    def resizeGL(self, w, h):
        self.update_projection()