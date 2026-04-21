# viewers/viewer_rendering.py
import numpy as np
from PyQt5.QtGui import QCursor, QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Import des constantes de configuration
from config.settings import (
    GRID_SIZE, GRID_SPACING, GRID_MAJOR_EVERY,
    GRID_COLOR_MINOR, GRID_COLOR_MAJOR,
    GRID_LINE_WIDTH_MINOR, GRID_LINE_WIDTH_MAJOR,
    AXE_X_VISIBLE, AXE_Y_VISIBLE, AXE_Z_VISIBLE,
    AXE_LINE_WIDTH,
    C_RED, C_GREEN, C_BLUE
)
from .gizmo import Gizmo
from utils.logger import debug_log

class ViewerRendering:
    """
    Mixin de rendu pour le Viewer3D.
    Cette classe gère les fonctions de dessin OpenGL et la projection.
    """

    def _create_nav_cursor(self, type):
        """Crée un curseur personnalisé pour le zoom ou le pan"""
        is_debug = getattr(self, 'debug', False)
        debug_log("Rendering", f"Création du curseur : {type}", is_debug)
        
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        p = QPainter(pixmap)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(QPen(QColor(200, 200, 200), 2))
        p.setBrush(QColor(60, 60, 60, 200))
        p.drawEllipse(2, 2, 28, 28)
        p.setPen(QPen(QColor(255, 255, 255), 2))
        
        if type == "zoom":
            # Icône Loupe / Zoom
            p.drawLine(16, 8, 16, 24)
            p.drawPolyline(QPoint(12, 12), QPoint(16, 8), QPoint(20, 12))
        else:
            # Icône Main / Pan (Croix)
            p.drawLine(8, 16, 24, 16)
            p.drawLine(16, 8, 16, 24)
            
        p.end()
        return QCursor(pixmap, 16, 16)

    def update_projection(self):
        """Met à jour la matrice de projection (Perspective ou Ortho)"""
        is_debug = getattr(self, 'debug', False)
        w, h = max(1, self.width()), max(1, self.height())
        
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / h

        if self.is_ortho:
            # Calcul de l'échelle ortho basé sur le zoom
            scale = abs(self.zoom) * 0.4
            glOrtho(-scale * aspect, scale * aspect, -scale, scale, 0.1, 1000.0)
            debug_log("Rendering", f"Projection: ORTHO (Echelle: {scale:.2f})", is_debug)
        else:
            # Perspective standard
            gluPerspective(45, aspect, 0.1, 1000.0)
            debug_log("Rendering", f"Projection: PERSP (Zoom: {self.zoom:.2f})", is_debug)
            
        glMatrixMode(GL_MODELVIEW)

    def draw_grid(self):
        """Dessine une grille au sol basée sur GRID_SIZE et GRID_SPACING"""
        size = GRID_SIZE
        step = GRID_SPACING
        
        # Calcul du nombre de lignes
        num_lines = int(size / step)
        
        # 1. Lignes secondaires (fines)
        glLineWidth(GRID_LINE_WIDTH_MINOR)
        glColor4f(*GRID_COLOR_MINOR)
        glBegin(GL_LINES)
        
        for i in range(-num_lines, num_lines + 1):
            v = i * step
            # Ignorer les lignes majeures (elles seront dessinées après)
            if GRID_MAJOR_EVERY > 0 and i % GRID_MAJOR_EVERY == 0 and i != 0:
                continue
            
            glVertex3f(-size, 0, v)
            glVertex3f(size, 0, v)
            glVertex3f(v, 0, -size)
            glVertex3f(v, 0, size)
        glEnd()
        
        # 2. Lignes majeures (plus épaisses)
        if GRID_MAJOR_EVERY > 0:
            glLineWidth(GRID_LINE_WIDTH_MAJOR)
            glColor4f(*GRID_COLOR_MAJOR)
            glBegin(GL_LINES)
            
            for i in range(-num_lines, num_lines + 1):
                if i == 0:
                    continue
                if i % GRID_MAJOR_EVERY == 0:
                    v = i * step
                    glVertex3f(-size, 0, v)
                    glVertex3f(size, 0, v)
                    glVertex3f(v, 0, -size)
                    glVertex3f(v, 0, size)
            glEnd()

    def draw_world_axes(self):
        """Dessine les axes XYZ selon la configuration de visibilité"""
        glLineWidth(AXE_LINE_WIDTH)
        # Légère décalage de profondeur pour éviter le clignotement avec la grille
        glDepthRange(0.0, 0.999)
        glBegin(GL_LINES)
        
        # Axe X (Rouge)
        if AXE_X_VISIBLE:
            glColor3f(*C_RED)
            glVertex3f(-GRID_SIZE, 0, 0)
            glVertex3f(GRID_SIZE, 0, 0)
            
        # Axe Y (Vert)
        if AXE_Y_VISIBLE:
            glColor3f(*C_GREEN)
            glVertex3f(0, -GRID_SIZE, 0)
            glVertex3f(0, GRID_SIZE, 0)
            
        # Axe Z (Bleu)
        if AXE_Z_VISIBLE:
            glColor3f(*C_BLUE)
            glVertex3f(0, 0, -GRID_SIZE)
            glVertex3f(0, 0, GRID_SIZE)
            
        glEnd()
        glDepthRange(0.0, 1.0)

    def draw_cube_centered(self):
        """Dessine un cube de test au centre du monde"""
        glLineWidth(2.0)
        s = 1.0  # Taille
        v = [
            [-s, -s, -s], [s, -s, -s], [s, s, -s], [-s, s, -s],
            [-s, -s, s], [s, -s, s], [s, s, s], [-s, s, s]
        ]
        e = [
            (0,1), (1,2), (2,3), (3,0), # Face arrière
            (4,5), (5,6), (6,7), (7,4), # Face avant
            (0,4), (1,5), (2,6), (3,7)  # Liaisons
        ]
        glBegin(GL_LINES)
        glColor3f(0.8, 0.8, 0.8) # Gris clair
        for edge in e:
            for vertex in edge:
                glVertex3fv(v[vertex])
        glEnd()