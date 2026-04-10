# viewers/main_viewer.py

import numpy as np
from PyQt5.QtWidgets import QOpenGLWidget, QMenu
from PyQt5.QtCore import Qt, QPoint
from OpenGL.GL import *
from OpenGL.GLU import *
from config.settings import *
from .gizmo import Gizmo

class Viewer3D(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.angle_x = 25.0  
        self.angle_z = -45.0 
        self.zoom = -12.0
        self.last_pos = QPoint()

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(*C_BG)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, self.zoom)
        glRotatef(self.angle_x, 1, 0, 0)
        glRotatef(self.angle_z, 0, 1, 0)
        
        model_view = glGetFloatv(GL_MODELVIEW_MATRIX)

        self.draw_grid()
        self.draw_world_axes()
        self.draw_cube_centered() 
        Gizmo.render(self.width(), self.height(), model_view)

    def draw_grid(self):
        glLineWidth(1.0)
        glColor4f(*C_GRID)
        size = 10 * UNIT
        steps = 10
        glBegin(GL_LINES)
        for i in range(-steps, steps + 1):
            v = i * (size/steps)
            glVertex3f(-size, 0, v); glVertex3f(size, 0, v)
            glVertex3f(v, 0, -size); glVertex3f(v, 0, size)
        glEnd()

    def draw_world_axes(self):
        glLineWidth(2.5)
        glBegin(GL_LINES)
        glColor3f(*C_RED);   glVertex3f(-10 * UNIT, 0, 0); glVertex3f(10 * UNIT, 0, 0)
        glColor3f(*C_GREEN); glVertex3f(0, 0, -10 * UNIT); glVertex3f(0, 0, 10 * UNIT)
        glEnd()

    def draw_cube_centered(self):
        glLineWidth(2.0)
        s = UNIT 
        v = [[-s,-s,-s], [s,-s,-s], [s,s,-s], [-s,s,-s], [-s,-s,s], [s,-s,s], [s,s,s], [-s,s,s]]
        e = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
        glBegin(GL_LINES)
        glColor3f(0.9, 0.9, 0.9)
        for edge in e:
            for vertex in edge: glVertex3fv(v[vertex])
        glEnd()

    def wheelEvent(self, event):
        self.zoom += event.angleDelta().y() * 0.005
        self.update()

    def mousePressEvent(self, event):
        self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MidButton:
            diff = event.pos() - self.last_pos
            self.last_pos = event.pos()
            self.angle_z += diff.x() * 0.5
            self.angle_x += diff.y() * 0.5
            self.angle_x = max(-90, min(90, self.angle_x))
            self.update()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / max(1, h), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)