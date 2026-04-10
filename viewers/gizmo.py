# /viewers/gizmo.py

from OpenGL.GL import *
import numpy as np
import math
from config.settings import *

class Gizmo:
    @staticmethod
    def draw_letter(char, pos, color):
        """Dessine une lettre en segments GL_LINES (taille réduite)."""
        s = L_SIZE * 0.7 
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        glColor3f(*color)
        glLineWidth(L_WIDTH)
        glBegin(GL_LINES)
        if char == 'X':
            glVertex3f(-s, -s, 0); glVertex3f(s, s, 0)
            glVertex3f(s, -s, 0); glVertex3f(-s, s, 0)
        elif char == 'Y':
            glVertex3f(-s, s, 0); glVertex3f(0, 0, 0)
            glVertex3f(s, s, 0); glVertex3f(0, 0, 0)
            glVertex3f(0, 0, 0); glVertex3f(0, -s, 0)
        elif char == 'Z':
            glVertex3f(-s, s, 0); glVertex3f(s, s, 0)
            glVertex3f(s, s, 0); glVertex3f(-s, -s, 0)
            glVertex3f(-s, -s, 0); glVertex3f(s, -s, 0)
        glEnd()
        glPopMatrix()

    @staticmethod
    def draw_dot(pos, color):
        """Dessine un rond coloré : contour 1px pur et intérieur transparent."""
        # Encore plus grand : 1.2 x la taille de référence
        radius = L_SIZE * 1.2 
        segments = 32
        
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        
        # 1. Intérieur transparent (Alpha 0.3)
        glBegin(GL_TRIANGLE_FAN)
        glColor4f(color[0], color[1], color[2], 0.3)
        glVertex3f(0, 0, 0)
        for i in range(segments + 1):
            theta = 2.0 * math.pi * float(i) / float(segments)
            glVertex3f(radius * math.cos(theta), radius * math.sin(theta), 0)
        glEnd()
        
        # 2. Contour pur (1 pixel)
        glLineWidth(1.0)
        glBegin(GL_LINE_LOOP)
        glColor4f(color[0], color[1], color[2], 1.0)
        for i in range(segments):
            theta = 2.0 * math.pi * float(i) / float(segments)
            glVertex3f(radius * math.cos(theta), radius * math.sin(theta), 0)
        glEnd()
        
        glPopMatrix()

    @staticmethod
    def render(width, height, model_view_matrix):
        """Affiche le Gizmo style Blender (décalé vers le bas)."""
        rot_only = np.copy(model_view_matrix)
        rot_only[3][0:3] = 0 
        
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        aspect = width / height
        glOrtho(-aspect, aspect, -1, 1, -10, 10)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # POSITIONNEMENT : G_TOP est diminué de 0.05 (~5 pixels en espace normalisé)
        # On passe de 0.85 à 0.80 pour descendre le bloc
        y_offset = G_TOP - 0.05
        glTranslatef(aspect - G_RIGHT, y_offset, 0)
        
        glMultMatrixf(rot_only)
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_DEPTH_TEST)
        
        axis_len = 0.06
        letter_offset = axis_len + 0.07 # Ajusté pour les cercles plus grands
        
        # --- 1. AXES POSITIFS ---
        glLineWidth(2.5)
        glBegin(GL_LINES)
        glColor3f(*C_RED);   glVertex3f(0, 0, 0); glVertex3f(axis_len, 0, 0)
        glColor3f(*C_GREEN); glVertex3f(0, 0, 0); glVertex3f(0, 0, axis_len)
        glColor3f(*C_BLUE);  glVertex3f(0, 0, 0); glVertex3f(0, axis_len, 0)
        glEnd()

        # --- 2. LETTRES (Positifs) ---
        Gizmo.draw_letter('X', [letter_offset, 0, 0], C_RED)
        Gizmo.draw_letter('Z', [0, letter_offset, 0], C_BLUE)
        Gizmo.draw_letter('Y', [0, 0, letter_offset], C_GREEN)

        # --- 3. RONDS (Négatifs) ---
        Gizmo.draw_dot([-letter_offset, 0, 0], C_RED)    # -X
        Gizmo.draw_dot([0, -letter_offset, 0], C_BLUE)   # -Z
        Gizmo.draw_dot([0, 0, -letter_offset], C_GREEN)  # -Y
        
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)