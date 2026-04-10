# /viewers/gizmo.py

from OpenGL.GL import *
import numpy as np
import math
from config.settings import *

class Gizmo:
    @staticmethod
    def draw_letter_mask(char, s):
        """Dessine la silhouette de la lettre."""
        glLineWidth(L_WIDTH * 1.8) # Un poil plus fin car la lettre est plus petite
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
    def draw_interactive_dot(pos, color, char=None):
        """ Pastille un peu plus petite. """
        # Réduction de 1.5 à 1.3
        radius = L_SIZE * 1.3 
        s_letter = radius * 0.5 
        
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        
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
        """Affiche le Gizmo plus compact et décalé vers la gauche."""
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
        
        # --- POSITIONNEMENT ---
        # y_pos : reste à -0.08 (3px plus bas que précédemment)
        # x_pos : On augmente la soustraction de G_RIGHT pour pousser vers la gauche
        # On passe de (G_RIGHT - 0.03) à (G_RIGHT + 0.02) pour gagner environ 5 pixels vers la gauche
        y_pos = G_TOP - 0.04
        x_pos = aspect - (G_RIGHT + 0.02) 
        glTranslatef(x_pos, y_pos, 0)
        
        glMultMatrixf(rot_only)
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_DEPTH_TEST) 
        
        # ... (le reste du code des axes et pastilles demeure inchangé)
        
        axis_len = 0.06
        dot_off = axis_len + 0.08 
        
        # Axes
        glLineWidth(2.5)
        glBegin(GL_LINES)
        glColor3f(*C_RED);   glVertex3f(0, 0, 0); glVertex3f(axis_len, 0, 0)
        glColor3f(*C_GREEN); glVertex3f(0, 0, 0); glVertex3f(0, 0, axis_len)
        glColor3f(*C_BLUE);  glVertex3f(0, 0, 0); glVertex3f(0, axis_len, 0)
        glEnd()

        glStencilMask(0xFF)
        glClear(GL_STENCIL_BUFFER_BIT)

        # Pastilles Positives
        Gizmo.draw_interactive_dot([dot_off, 0, 0], C_RED, char='X')
        Gizmo.draw_interactive_dot([0, dot_off, 0], C_BLUE, char='Z')
        Gizmo.draw_interactive_dot([0, 0, dot_off], C_GREEN) 

        # Pastilles Négatives
        Gizmo.draw_interactive_dot([-dot_off, 0, 0], C_RED)
        Gizmo.draw_interactive_dot([0, -dot_off, 0], C_BLUE)
        Gizmo.draw_interactive_dot([0, 0, -dot_off], C_GREEN, char='Y')

        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)