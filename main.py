import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget, QDesktopWidget, QMessageBox
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QSurfaceFormat
from OpenGL.GL import *
from OpenGL.GLU import *

# ==========================================
# CONFIGURATION GLOBALE
# ==========================================
T_APP     = "K3D viewer"
UNIT      = 1.0    
G_SCALE   = 0.2    
G_TOP     = 0.85   
G_RIGHT   = 0.16   
L_SIZE    = 0.02   
L_WIDTH   = 1.5    

# Couleurs (R, G, B)
C_RED     = (1.0, 0.22, 0.26) # Axe X
C_GREEN   = (0.55, 0.85, 0.1) # Axe Y
C_BLUE    = (0.18, 0.52, 1.0) # Axe Z (Vertical)
C_GRID    = (0.4, 0.4, 0.4, 0.6) # (R, G, B, Alpha) - Plus visible
# ==========================================

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
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        
        # Activation du blending pour la transparence de la grille
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glClearColor(0.12, 0.12, 0.12, 1.0)

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
        self.draw_gizmo(model_view)

    def draw_grid(self):
        glLineWidth(1.0)
        glColor4f(*C_GRID) # Utilisation de la variable globale
        size = 10 * UNIT
        steps = 10
        glBegin(GL_LINES)
        for i in range(-steps, steps + 1):
            v = i * (size/steps)
            # Plan XZ
            glVertex3f(-size, 0, v); glVertex3f(size, 0, v)
            glVertex3f(v, 0, -size); glVertex3f(v, 0, size)
        glEnd()

    def draw_world_axes(self):
        glLineWidth(2.5)
        glBegin(GL_LINES)
        glColor3f(*C_RED)   # X
        glVertex3f(-10 * UNIT, 0, 0); glVertex3f(10 * UNIT, 0, 0)
        glColor3f(*C_GREEN) # Y
        glVertex3f(0, 0, -10 * UNIT); glVertex3f(0, 0, 10 * UNIT)
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

    def draw_gizmo(self, model_view):
        rot_only = np.copy(model_view)
        rot_only[3][0:3] = 0 
        
        width, height = self.width(), self.height()
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        aspect = width / height
        glOrtho(-aspect, aspect, -1, 1, -10, 10)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glTranslatef(aspect - G_RIGHT, G_TOP, 0)
        glMultMatrixf(rot_only)
        
        length = 0.3 * G_SCALE
        glDisable(GL_DEPTH_TEST)
        glLineWidth(2.5)
        
        glBegin(GL_LINES)
        glColor3f(*C_RED);   glVertex3f(0,0,0); glVertex3f(length,0,0) # X
        glColor3f(*C_GREEN); glVertex3f(0,0,0); glVertex3f(0,0,length) # Y
        glColor3f(*C_BLUE);  glVertex3f(0,0,0); glVertex3f(0,length,0) # Z
        glEnd()
        
        offset = length + (L_SIZE * 2)
        self.draw_letter('X', [offset, 0, 0], C_RED)
        self.draw_letter('Z', [0, offset, 0], C_BLUE)
        self.draw_letter('Y', [0, 0, offset], C_GREEN)
        
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    def draw_letter(self, char, pos, color):
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        glColor3f(*color)
        glLineWidth(L_WIDTH)
        glBegin(GL_LINES)
        if char == 'X':
            glVertex3f(-L_SIZE, -L_SIZE, 0); glVertex3f(L_SIZE, L_SIZE, 0)
            glVertex3f(L_SIZE, -L_SIZE, 0); glVertex3f(-L_SIZE, L_SIZE, 0)
        elif char == 'Y':
            glVertex3f(-L_SIZE, L_SIZE, 0); glVertex3f(0, 0, 0)
            glVertex3f(L_SIZE, L_SIZE, 0); glVertex3f(0, 0, 0)
            glVertex3f(0, 0, 0); glVertex3f(0, -L_SIZE, 0)
        elif char == 'Z':
            glVertex3f(-L_SIZE, L_SIZE, 0); glVertex3f(L_SIZE, L_SIZE, 0)
            glVertex3f(L_SIZE, L_SIZE, 0); glVertex3f(-L_SIZE, -L_SIZE, 0)
            glVertex3f(-L_SIZE, -L_SIZE, 0); glVertex3f(L_SIZE, -L_SIZE, 0)
        glEnd()
        glPopMatrix()

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        fmt = QSurfaceFormat()
        fmt.setSamples(8) 
        QSurfaceFormat.setDefaultFormat(fmt)
        
        self.viewer = Viewer3D()
        self.setCentralWidget(self.viewer)
        self.setWindowTitle(T_APP)
        
        screen = QDesktopWidget().availableGeometry()
        self.resize(int(screen.width()*0.8), int(screen.height()*0.8))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())