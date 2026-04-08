# // main.py
import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget, QDesktopWidget
from PyQt5.QtCore import Qt, QPoint
from OpenGL.GL import *
from OpenGL.GLU import *

# ==========================================
# CONFIGURATION GLOBALE
# ==========================================
UNIT        = 1.0    # Taille de référence
# --- GIZMO ---
G_SCALE     = 0.2    # Taille globale du Gizmo
G_TOP       = 0.85   # Position Y (0=bas, 1=haut)
G_RIGHT     = 0.16   # Position X (marge droite)
# --- LETTRES ---
L_SIZE      = 0.02   # Taille des lettres X, Y, Z
L_WIDTH     = 1.5    # Épaisseur du trait des lettres
# ==========================================

class Quaternion:
    def __init__(self, w=1.0, x=0.0, y=0.0, z=0.0):
        self.w, self.x, self.y, self.z = w, x, y, z

    def to_matrix(self):
        w, x, y, z = self.w, self.x, self.y, self.z
        return np.array([
            [1 - 2*y**2 - 2*z**2, 2*x*y - 2*z*w,     2*x*z + 2*y*w,     0],
            [2*x*y + 2*z*w,     1 - 2*x**2 - 2*z**2, 2*y*z - 2*x*w,     0],
            [2*x*z - 2*y*w,     2*y*z + 2*x*w,     1 - 2*x**2 - 2*y**2, 0],
            [0,                 0,                 0,                 1]
        ], dtype=np.float32)

    @staticmethod
    def from_axis_angle(axis, angle_rad):
        s = np.sin(angle_rad / 2.0)
        norm = np.linalg.norm(axis)
        if norm < 1e-6: return Quaternion()
        axis = axis / norm
        return Quaternion(np.cos(angle_rad / 2.0), axis[0]*s, axis[1]*s, axis[2]*s)

    def __mul__(self, other):
        w1, x1, y1, z1 = self.w, self.x, self.y, self.z
        w2, x2, y2, z2 = other.w, other.x, other.y, other.z
        return Quaternion(
            w1*w2 - x1*x2 - y1*y2 - z1*z2,
            w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2,
            w1*z2 + x1*y2 - y1*x2 + z1*w2
        )

class Viewer3D(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.cur_quat = Quaternion()
        self.last_pos = QPoint()
        self.zoom = -12.0
        # Désactive le menu contextuel par défaut pour libérer le clic droit
        self.setContextMenuPolicy(Qt.NoContextMenu)

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LINE_SMOOTH)
        glClearColor(0.12, 0.12, 0.12, 1.0)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Vue caméra
        glTranslatef(0.0, 0.0, self.zoom)
        glRotatef(25, 1, 0, 0)
        glRotatef(-45, 0, 1, 0)
        
        # Rotation interactive
        rot_matrix = self.cur_quat.to_matrix().T
        glMultMatrixf(rot_matrix)
        
        self.draw_grid()
        self.draw_world_axes()
        self.draw_cube_centered() 
        self.draw_gizmo(rot_matrix)

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

    def draw_gizmo(self, rot_matrix):
        width, height = self.width(), self.height()
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        aspect = width / height
        glOrtho(-aspect, aspect, -1, 1, -10, 10)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Positionnement dans l'écran
        glTranslatef(aspect - G_RIGHT, G_TOP, 0)
        
        # Même orientation que la scène
        glRotatef(25, 1, 0, 0)
        glRotatef(-45, 0, 1, 0)
        glMultMatrixf(rot_matrix)
        
        length = 0.3 * G_SCALE
        glDisable(GL_DEPTH_TEST)
        glLineWidth(2.0)
        
        glBegin(GL_LINES)
        glColor3f(1.0, 0.2, 0.2); glVertex3f(0,0,0); glVertex3f(length,0,0) # X
        glColor3f(0.2, 1.0, 0.2); glVertex3f(0,0,0); glVertex3f(0,length,0) # Y
        glColor3f(0.2, 0.6, 1.0); glVertex3f(0,0,0); glVertex3f(0,0,length) # Z
        glEnd()

        offset = length + (L_SIZE * 1.5)
        self.draw_letter('X', [offset, 0, 0], [1.0, 0.2, 0.2])
        self.draw_letter('Y', [0, offset, 0], [0.2, 1.0, 0.2])
        self.draw_letter('Z', [0, 0, offset], [0.2, 0.6, 1.0])
        
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    def draw_grid(self):
        glLineWidth(1)
        glColor3f(0.2, 0.2, 0.2)
        size = 10 * UNIT
        steps = 10
        glBegin(GL_LINES)
        for i in range(-steps, steps + 1):
            v = i * (size/steps)
            glVertex3f(-size, 0, v); glVertex3f(size, 0, v)
            glVertex3f(v, 0, -size); glVertex3f(v, 0, size)
        glEnd()

    def draw_world_axes(self):
        glLineWidth(2)
        glBegin(GL_LINES)
        glColor3f(0.4, 0.1, 0.1); glVertex3f(-10, 0, 0); glVertex3f(10, 0, 0) # X
        glColor3f(0.1, 0.1, 0.4); glVertex3f(0, 0, -10); glVertex3f(0, 0, 10) # Z
        glColor3f(0.1, 0.4, 0.1); glVertex3f(0, -10, 0); glVertex3f(0, 10, 0) # Y
        glEnd()

    def draw_cube_centered(self):
        glLineWidth(2)
        s = UNIT 
        v = [[-s,-s,-s], [s,-s,-s], [s,s,-s], [-s,s,-s], [-s,-s,s], [s,-s,s], [s,s,s], [-s,s,s]]
        e = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
        glBegin(GL_LINES)
        glColor3f(1.0, 1.0, 1.0)
        for edge in e:
            for vertex in edge: glVertex3fv(v[vertex])
        glEnd()

    def wheelEvent(self, event):
        self.zoom += event.angleDelta().y() * 0.005
        self.update()

    def mousePressEvent(self, event):
        # On stocke la position quel que soit le bouton pour les deltas
        self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        # Rotation activée uniquement par la molette (bouton du milieu)
        if event.buttons() & Qt.MidButton:
            diff = event.pos() - self.last_pos
            self.last_pos = event.pos()
            
            axis = np.array([diff.y(), diff.x(), 0.0], dtype=float)
            angle = np.linalg.norm(axis) * 0.005
            
            if angle > 0:
                delta_quat = Quaternion.from_axis_angle(axis, angle)
                self.cur_quat = delta_quat * self.cur_quat
                self.update()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / max(1, h), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Géométrie centrée sur l'écran à 80% de taille
    screen = QDesktopWidget().availableGeometry()
    w, h = int(screen.width() * 0.8), int(screen.height() * 0.8)
    
    win = QMainWindow()
    win.setCentralWidget(Viewer3D())
    win.setWindowTitle("K3Dviewer - Middle Mouse to Orbit")
    win.resize(w, h)
    win.move(int((screen.width() - w) / 2), int((screen.height() - h) / 2))
    win.show()
    
    sys.exit(app.exec_())