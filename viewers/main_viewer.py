# viewers/main_viewer.py
import numpy as np
from PyQt5.QtWidgets import QOpenGLWidget, QApplication
from PyQt5.QtCore import Qt, QPoint
from OpenGL.GL import *
from OpenGL.GLU import *
from config.settings import *
from .gizmo import Gizmo
from menus.context_menu import MainContextMenu

class Viewer3D(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.def_zoom = -12.0
        self.zoom = self.def_zoom
        self.pan_x, self.pan_y = 0.0, 0.0
        
        # Stockage séparé des angles pour le mode "Turntable" (Blender style)
        self.rot_x = 25.0  # Inclinaison haut/bas
        self.rot_y = -45.0 # Rotation gauche/droite (autour du monde)
        
        self.last_pos = QPoint()
        self.is_ortho = False
        self.show_grid = True
        self.context_menu = MainContextMenu(self)

    def set_projection(self, ortho_mode):
        self.is_ortho = ortho_mode
        self.makeCurrent()
        self.update_projection()
        self.update()

    def set_grid_visible(self, visible):
        self.show_grid = visible
        self.update()

    def reset_view(self):
        self.makeCurrent()
        self.zoom = self.def_zoom
        self.pan_x, self.pan_y = 0.0, 0.0
        self.rot_x = 25.0
        self.rot_y = -45.0
        self.update_projection()
        self.update()

    def update_projection(self):
        w, h = self.width(), self.height()
        if h == 0: h = 1
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / h
        if self.is_ortho:
            scale = abs(self.zoom) * 0.5
            glOrtho(-scale * aspect, scale * aspect, -scale, scale, 0.1, 1000.0)
        else:
            gluPerspective(45, aspect, 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # 1. Positionnement Caméra
        glTranslatef(self.pan_x, self.pan_y, self.zoom)
        
        # 2. Rotation Turntable (Blender Style)
        # On applique d'abord l'inclinaison (X), 
        # puis la rotation autour de l'axe vertical du monde (Y)
        glRotatef(self.rot_x, 1, 0, 0)
        glRotatef(self.rot_y, 0, 1, 0)
        
        mv_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        # 3. Dessin
        if self.show_grid: self.draw_grid()
        self.draw_world_axes()
        self.draw_cube_centered() 
        
        # 4. Gizmo
        glDisable(GL_DEPTH_TEST)
        Gizmo.render(self.width(), self.height(), mv_matrix)
        glEnable(GL_DEPTH_TEST)

    def draw_grid(self):
        size = 10 * UNIT
        main_div, sub_div = 10, 50
        glLineWidth(1.0)
        glColor4f(0.28, 0.28, 0.28, 0.15)
        glBegin(GL_LINES)
        for i in range(-sub_div, sub_div + 1):
            if i % 5 == 0: continue
            v = i * (size / sub_div)
            glVertex3f(-size, 0, v); glVertex3f(size, 0, v)
            glVertex3f(v, 0, -size); glVertex3f(v, 0, size)
        glEnd()
        glLineWidth(1.5)
        glColor4f(0.28, 0.28, 0.28, 0.4)
        glBegin(GL_LINES)
        for i in range(-main_div, main_div + 1):
            if i == 0: continue
            v = i * (size / main_div)
            glVertex3f(-size, 0, v); glVertex3f(size, 0, v)
            glVertex3f(v, 0, -size); glVertex3f(v, 0, size)
        glEnd()

    def draw_world_axes(self):
        glLineWidth(2.0)
        glBegin(GL_LINES)
        glColor3f(*C_RED); glVertex3f(-10, 0, 0); glVertex3f(10, 0, 0)
        glColor3f(*C_GREEN); glVertex3f(0, 0, -10); glVertex3f(0, 0, 10)
        glEnd()

    def draw_cube_centered(self):
        glLineWidth(2.0)
        s = UNIT
        v = [[-s,-s,-s], [s,-s,-s], [s,s,-s], [-s,s,-s], [-s,-s,s], [s,-s,s], [s,s,s], [-s,s,s]]
        e = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
        glBegin(GL_LINES)
        glColor3f(0.8, 0.8, 0.8)
        for edge in e:
            for vertex in edge: glVertex3fv(v[vertex])
        glEnd()

    def wheelEvent(self, event):
        self.zoom += event.angleDelta().y() * 0.005
        if self.is_ortho: self.update_projection()
        self.update()

    def mouseMoveEvent(self, event):
            diff = event.pos() - self.last_pos
            self.last_pos = event.pos()

            if event.buttons() & Qt.MidButton:
                if QApplication.keyboardModifiers() & Qt.ShiftModifier:
                    # PANNING reste inchangé
                    factor = abs(self.zoom) * 0.001
                    self.pan_x += diff.x() * factor
                    self.pan_y -= diff.y() * factor
                else:
                    # ROTATION TOTALE (sans limites)
                    self.rot_y += diff.x() * 0.5
                    self.rot_x += diff.y() * 0.5  # <--- Suppression du max/min ici
                
                self.update()

    def mousePressEvent(self, event):
        self.last_pos = event.pos()

    def resizeGL(self, w, h):
        self.update_projection()

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(*C_BG)