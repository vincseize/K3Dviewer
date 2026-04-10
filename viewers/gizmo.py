# /viewers/gizmo.py

from OpenGL.GL import *
import numpy as np
import math
from config.settings import *

class Gizmo:
    @staticmethod
    def draw_letter_mask(char, s):
        """Dessine la silhouette de la lettre."""
        glLineWidth(L_WIDTH * 1.8)
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

    @staticmethod
    def draw_filled_circle(radius, color, alpha=1.0, segments=32):
        glBegin(GL_TRIANGLE_FAN)
        glColor4f(color[0], color[1], color[2], alpha)
        glVertex3f(0, 0, 0)
        for i in range(segments + 1):
            theta = 2.0 * math.pi * float(i) / float(segments)
            glVertex3f(radius * math.cos(theta), radius * math.sin(theta), 0)
        glEnd()

    @staticmethod
    def draw_circle_outline(radius, color, alpha=1.0, segments=32):
        glLineWidth(1.0)
        glBegin(GL_LINE_LOOP)
        glColor4f(color[0], color[1], color[2], alpha)
        for i in range(segments):
            theta = 2.0 * math.pi * float(i) / float(segments)
            glVertex3f(radius * math.cos(theta), radius * math.sin(theta), 0)
        glEnd()

    @staticmethod
    def draw_interactive_dot(pos, color, rot_inv, char=None):
        """ Dessine une pastille qui fait face à la caméra (Billboarding). """
        radius = L_SIZE * 1.3 
        s_letter = radius * 0.5 
        
        glPushMatrix()
        # On se déplace à la position 3D de l'axe
        glTranslatef(pos[0], pos[1], pos[2])
        
        # --- BILLBOARDING ---
        # On annule la rotation de la scène pour que le cercle soit face écran
        glMultMatrixf(rot_inv)
        
        if char:
            glEnable(GL_STENCIL_TEST)
            glStencilMask(0xFF) 
            glStencilFunc(GL_ALWAYS, 1, 0xFF)
            glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)
            glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)
            glDisable(GL_DEPTH_TEST)
            
            Gizmo.draw_letter_mask(char, s_letter)
            
            glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
            glStencilFunc(GL_NOTEQUAL, 1, 0xFF) 
            glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP) 
            
            Gizmo.draw_filled_circle(radius, color, alpha=1.0)
            Gizmo.draw_circle_outline(radius, color, alpha=1.0)
            glDisable(GL_STENCIL_TEST)
        else:
            Gizmo.draw_filled_circle(radius, color, alpha=0.3)
            Gizmo.draw_circle_outline(radius, color, alpha=1.0)
            
        glPopMatrix()

    @staticmethod
    def render(width, height, model_view_matrix):
        """Affiche le Gizmo avec billboarding complet."""
        # Matrice de rotation
        rot_only = np.copy(model_view_matrix)
        rot_only[3][0:3] = 0 
        
        # Inverse de la rotation (Transposée) pour le Billboarding
        rot_inv = np.copy(rot_only.T)
        
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        aspect = width / height
        glOrtho(-aspect, aspect, -1, 1, -10, 10)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Positionnement
        y_pos = G_TOP - 0.04
        x_pos = aspect - (G_RIGHT + 0.02) 
        glTranslatef(x_pos, y_pos, 0)
        
        # On applique la rotation pour les traits des axes
        glPushMatrix()
        glMultMatrixf(rot_only)
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_DEPTH_TEST) 
        
        axis_len = 0.06
        dot_off = axis_len + 0.08 
        
        # --- 1. AXES (TRAITS) ---
        glLineWidth(2.5)
        glBegin(GL_LINES)
        glColor3f(*C_RED);   glVertex3f(0, 0, 0); glVertex3f(axis_len, 0, 0)
        glColor3f(*C_GREEN); glVertex3f(0, 0, 0); glVertex3f(0, 0, axis_len)
        glColor3f(*C_BLUE);  glVertex3f(0, 0, 0); glVertex3f(0, axis_len, 0)
        glEnd()

        glStencilMask(0xFF)
        glClear(GL_STENCIL_BUFFER_BIT)

        # --- 2. PASTILLES (Avec rot_inv passé pour le Billboarding) ---
        # Positives
        Gizmo.draw_interactive_dot([dot_off, 0, 0], C_RED, rot_inv, char='X')
        Gizmo.draw_interactive_dot([0, dot_off, 0], C_BLUE, rot_inv, char='Z')
        Gizmo.draw_interactive_dot([0, 0, dot_off], C_GREEN, rot_inv) 

        # Négatives
        Gizmo.draw_interactive_dot([-dot_off, 0, 0], C_RED, rot_inv)
        Gizmo.draw_interactive_dot([0, -dot_off, 0], C_BLUE, rot_inv)
        Gizmo.draw_interactive_dot([0, 0, -dot_off], C_GREEN, rot_inv, char='Y')

        glPopMatrix() # Fin rotation traits
        
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)