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
        
        # Angles pour le mode "Turntable" (Blender style)
        self.rot_x = 25.0  # Inclinaison
        self.rot_y = -45.0 # Orbite
        
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
        
        # 2. Rotation Turntable
        glRotatef(self.rot_x, 1, 0, 0)
        glRotatef(self.rot_y, 0, 1, 0)
        
        mv_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        # 3. Dessin des éléments de scène DANS LE BON ORDRE
        # La grille en premier (en arrière-plan)
        if self.show_grid: 
            self.draw_grid()
        
        # Le cube avec écriture depth désactivée pour éviter le Z-fighting
        glDepthMask(GL_FALSE)  # Le cube n'écrit pas dans le depth buffer
        self.draw_cube_centered()
        glDepthMask(GL_TRUE)   # On réactive l'écriture depth pour la suite
        
        # Les axes toujours visibles par-dessus
        self.draw_world_axes()
        
        # 4. Rendu du Gizmo (Overlay)
        glDisable(GL_DEPTH_TEST)
        Gizmo.render(self.width(), self.height(), mv_matrix)
        glEnable(GL_DEPTH_TEST)

    def draw_grid(self):
        """Dessine la grille de référence."""
        size = 10 * UNIT
        main_div, sub_div = 10, 50
        
        # Lignes fines (subdivisions)
        glLineWidth(1.0)
        glColor4f(0.28, 0.28, 0.28, 0.15)
        glBegin(GL_LINES)
        for i in range(-sub_div, sub_div + 1):
            if i % 5 == 0: 
                continue
            v = i * (size / sub_div)
            glVertex3f(-size, 0, v)
            glVertex3f(size, 0, v)
            glVertex3f(v, 0, -size)
            glVertex3f(v, 0, size)
        glEnd()

        # Lignes principales (tous les 5)
        glLineWidth(1.5)
        glColor4f(0.28, 0.28, 0.28, 0.4)
        glBegin(GL_LINES)
        for i in range(-main_div, main_div + 1):
            if i == 0:  # On laisse l'axe principal pour draw_world_axes
                continue
            v = i * (size / main_div)
            glVertex3f(-size, 0, v)
            glVertex3f(size, 0, v)
            glVertex3f(v, 0, -size)
            glVertex3f(v, 0, size)
        glEnd()

    def draw_world_axes(self):
        """Dessine les axes X, Y, Z du monde avec correction de clignotement."""
        glLineWidth(2.5)
        
        # Sauvegarde et modification du depth range pour prioriser les axes
        glDepthRange(0.0, 0.999)
        
        glBegin(GL_LINES)
        # Axe X - Rouge
        glColor3f(*C_RED)
        glVertex3f(-10, 0, 0)
        glVertex3f(10, 0, 0)
        
        # Axe Y - Vert
        glColor3f(*C_GREEN)
        glVertex3f(0, -10, 0)
        glVertex3f(0, 10, 0)
        
        # Axe Z - Bleu
        glColor3f(*C_BLUE)
        glVertex3f(0, 0, -10)
        glVertex3f(0, 0, 10)
        glEnd()
        
        # Restauration du depth range
        glDepthRange(0.0, 1.0)

    def draw_cube_centered(self):
        """Dessine le cube sans conflit de profondeur."""
        glLineWidth(2.0)
        s = UNIT
        
        # Sommets du cube
        v = [
            [-s, -s, -s], [s, -s, -s], [s, s, -s], [-s, s, -s],  # Face arrière
            [-s, -s, s], [s, -s, s], [s, s, s], [-s, s, s]       # Face avant
        ]
        
        # Arêtes du cube
        e = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Face arrière
            (4, 5), (5, 6), (6, 7), (7, 4),  # Face avant
            (0, 4), (1, 5), (2, 6), (3, 7)   # Connexions avant/arrière
        ]
        
        # Dessin des lignes
        glBegin(GL_LINES)
        glColor3f(0.8, 0.8, 0.8)  # Gris clair
        for edge in e:
            for vertex in edge:
                glVertex3fv(v[vertex])
        glEnd()

    def wheelEvent(self, event):
        """Gère la molette de la souris pour le zoom."""
        self.zoom += event.angleDelta().y() * 0.005
        if self.is_ortho: 
            self.update_projection()
        self.update()

    def mouseMoveEvent(self, event):
        """Gère les mouvements de la souris pour la rotation et le panning."""
        diff = event.pos() - self.last_pos
        self.last_pos = event.pos()

        if event.buttons() & Qt.MidButton:
            if QApplication.keyboardModifiers() & Qt.ShiftModifier:
                # Panning (déplacement latéral)
                factor = abs(self.zoom) * 0.001
                self.pan_x += diff.x() * factor
                self.pan_y -= diff.y() * factor
            else:
                # Rotation libre
                self.rot_y += diff.x() * 0.5
                self.rot_x += diff.y() * 0.5
            
            self.update()

    def mousePressEvent(self, event):
        """Enregistre la position initiale de la souris."""
        self.last_pos = event.pos()
        
        # Bouton droit pour le menu contextuel
        if event.button() == Qt.RightButton:
            self.context_menu.exec_(event.globalPos())

    def resizeGL(self, w, h):
        """Gère le redimensionnement de la vue."""
        self.update_projection()

    def initializeGL(self):
        """Initialise les paramètres OpenGL."""
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)  # Anti-aliasing
        glEnable(GL_BLEND)        # Transparence
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(*C_BG)       # Couleur de fond