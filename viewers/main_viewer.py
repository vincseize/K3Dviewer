# viewers/main_viewer.py
import numpy as np
from PyQt5.QtWidgets import QOpenGLWidget, QApplication, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QPoint
from OpenGL.GL import *
from OpenGL.GLU import *
from config.settings import *
from .gizmo import Gizmo
from menus.context_menu import MainContextMenu

class Viewer3D(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.def_zoom = -12.0
        self.zoom = self.def_zoom
        self.pan_x, self.pan_y = 0.0, 0.0
        
        # Angles pour le mode "Turntable" (Blender style)
        self.rot_x = 25.0  # Inclinaison
        self.rot_y = -45.0 # Orbite
        
        self.last_pos = QPoint()
        self.is_ortho = False
        self.show_grid = True
        self.context_menu = MainContextMenu(self)
        
        # Création de l'overlay (Bouton Reset uniquement)
        self.setup_overlay_buttons()

    def setup_overlay_buttons(self):
        """Crée le bouton circulaire Reset View en haut à droite."""
        self.button_container = QWidget(self)
        self.button_container.setStyleSheet("""
            QWidget { background: transparent; }
            QPushButton {
                background-color: rgba(60, 60, 60, 200);
                border: 1px solid rgba(100, 100, 100, 255);
                border-radius: 16px;
                color: white;
                font-size: 16px;
                min-width: 32px; max-width: 32px;
                min-height: 32px; max-height: 32px;
            }
            QPushButton:hover { background-color: rgba(80, 80, 80, 220); }
        """)
        
        layout = QVBoxLayout(self.button_container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.reset_button = QPushButton()
        self.reset_button.setText("↺")
        self.reset_button.setToolTip("Réinitialiser la vue")
        self.reset_button.clicked.connect(self.reset_view)
        layout.addWidget(self.reset_button)
        
    def resizeEvent(self, event):
        """Positionne le bouton d'overlay."""
        super().resizeEvent(event)
        button_size = 34
        x_pos = self.width() - button_size - 10
        y_pos = 20 
        self.button_container.setGeometry(x_pos, y_pos, button_size, button_size)
        self.button_container.raise_()

    # --- MÉTHODES DE CONTRÔLE (Appelées par main.py) ---

    def set_projection(self, ortho_mode):
        """Définit le mode de projection (True=Ortho, False=Persp)."""
        self.is_ortho = ortho_mode
        self.makeCurrent()
        self.update_projection()
        self.update()

    def set_grid_visible(self, visible):
        """Affiche ou masque la grille."""
        self.show_grid = visible
        self.update()

    def reset_view(self):
        """Réinitialise la position et les angles de la caméra."""
        self.makeCurrent()
        self.zoom = self.def_zoom
        self.pan_x, self.pan_y = 0.0, 0.0
        self.rot_x = 25.0
        self.rot_y = -45.0
        self.update_projection()
        self.update()

    # --- LOGIQUE OPENGL ---

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
        
        # Application de la transformation de vue
        glTranslatef(self.pan_x, self.pan_y, self.zoom)
        glRotatef(self.rot_x, 1, 0, 0)
        glRotatef(self.rot_y, 0, 1, 0)
        
        mv_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        # Dessin de la grille
        if self.show_grid: 
            self.draw_grid()
        
        # Dessin du cube (avec correction de clignotement)
        glDepthMask(GL_FALSE)
        self.draw_cube_centered()
        glDepthMask(GL_TRUE)
        
        # Dessin des axes mondiaux
        self.draw_world_axes()
        
        # Rendu du Gizmo en overlay 2D
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
        glLineWidth(2.5)
        glDepthRange(0.0, 0.999)
        glBegin(GL_LINES)
        glColor3f(*C_RED); glVertex3f(-10, 0, 0); glVertex3f(10, 0, 0)
        glColor3f(*C_BLUE); glVertex3f(0, 0, -10); glVertex3f(0, 0, 10)
        glEnd()
        glDepthRange(0.0, 1.0)

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

    # --- ÉVÉNEMENTS SOURIS ---

    def wheelEvent(self, event):
        self.zoom += event.angleDelta().y() * 0.005
        if self.is_ortho: self.update_projection()
        self.update()

    def mouseMoveEvent(self, event):
        diff = event.pos() - self.last_pos
        self.last_pos = event.pos()
        if event.buttons() & Qt.MidButton:
            if QApplication.keyboardModifiers() & Qt.ShiftModifier:
                factor = abs(self.zoom) * 0.001
                self.pan_x += diff.x() * factor
                self.pan_y -= diff.y() * factor
            else:
                self.rot_y += diff.x() * 0.5
                self.rot_x += diff.y() * 0.5
            self.update()

    def mousePressEvent(self, event):
        self.last_pos = event.pos()
        if event.button() == Qt.RightButton:
            self.context_menu.exec_(event.globalPos())

    def resizeGL(self, w, h):
        self.update_projection()

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(*C_BG)