# viewers/viewer_rendering.py
import numpy as np
from PyQt5.QtGui import QCursor, QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from config.settings import *
from .gizmo import Gizmo
from utils.logger import debug_log

class ViewerRendering: # Mixin de rendu pour le Viewer3D, fille de ViewerCore? MainViewer?
    """
    Mixin de rendu pour le Viewer3D.
    Note : Cette classe n'a pas d'__init__ car elle est mixée dans Viewer3D.
    Elle utilise l'attribut 'self.debug' défini dans la classe parente.
    """

    def _create_nav_cursor(self, type):
        # On récupère le debug de la classe parente, sinon False par défaut
        is_debug = getattr(self, 'debug', False)
        debug_log("Rendering", f"Creating navigation cursor: {type}", is_debug)
        
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        p = QPainter(pixmap)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(QPen(QColor(200, 200, 200), 2))
        p.setBrush(QColor(60, 60, 60, 200))
        p.drawEllipse(2, 2, 28, 28)
        p.setPen(QPen(QColor(255, 255, 255), 2))
        
        if type == "zoom":
            p.drawLine(16, 8, 16, 24)
            p.drawPolyline(QPoint(12,12), QPoint(16,8), QPoint(20,12))
        else:
            p.drawLine(8, 16, 24, 16)
            p.drawLine(16, 8, 16, 24)
        p.end()
        return QCursor(pixmap, 16, 16)

    def update_projection(self):
        is_debug = getattr(self, 'debug', False)
        w, h = max(1, self.width()), max(1, self.height())
        
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / h

        if self.is_ortho:
            scale = abs(self.zoom) * 0.4
            glOrtho(-scale * aspect, scale * aspect, -scale, scale, 0.1, 1000.0)
            debug_log("Rendering", f"Projection: ORTHO (Scale: {scale:.2f})", is_debug)
        else:
            gluPerspective(45, aspect, 0.1, 1000.0)
            debug_log("Rendering", f"Projection: PERSP (Zoom: {self.zoom:.2f})", is_debug)
            
        glMatrixMode(GL_MODELVIEW)

    def draw_grid(self):
        size = 10
        glLineWidth(1.0)
        glColor4f(0.28, 0.28, 0.28, 0.15)
        glBegin(GL_LINES)
        for i in range(-50, 51):
            if i % 5 == 0: continue
            v = i * 0.2
            glVertex3f(-size, 0, v); glVertex3f(size, 0, v)
            glVertex3f(v, 0, -size); glVertex3f(v, 0, size)
        glEnd()
        
        glLineWidth(1.5)
        glColor4f(0.28, 0.28, 0.28, 0.4)
        glBegin(GL_LINES)
        for i in range(-10, 11):
            if i == 0: continue
            v = i
            glVertex3f(-size, 0, v); glVertex3f(size, 0, v)
            glVertex3f(v, 0, -size); glVertex3f(v, 0, size)
        glEnd()

    def draw_world_axes(self):
        glLineWidth(2.5)
        glDepthRange(0.0, 0.999)
        glBegin(GL_LINES)
        glColor3f(*C_RED); glVertex3f(-10, 0, 0); glVertex3f(10, 0, 0)
        glColor3f(*C_GREEN); glVertex3f(0, -10, 0); glVertex3f(0, 10, 0)
        glColor3f(*C_BLUE); glVertex3f(0, 0, -10); glVertex3f(0, 0, 10)
        glEnd()
        glDepthRange(0.0, 1.0)

    def draw_cube_centered(self):
        glLineWidth(2.0)
        s = 1.0
        v = [
            [-s, -s, -s], [s, -s, -s], [s, s, -s], [-s, s, -s],
            [-s, -s, s], [s, -s, s], [s, s, s], [-s, s, s]
        ]
        e = [
            (0,1), (1,2), (2,3), (3,0), (4,5), (5,6), 
            (6,7), (7,4), (0,4), (1,5), (2,6), (3,7)
        ]
        glBegin(GL_LINES)
        glColor3f(0.8, 0.8, 0.8)
        for edge in e:
            for vertex in edge:
                glVertex3fv(v[vertex])
        glEnd()