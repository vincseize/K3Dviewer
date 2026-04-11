# /viewers/gizmo.py
from OpenGL.GL import *
import numpy as np
import math
from config.settings import *

class Gizmo:
    @staticmethod
    def draw_letter_mask(char, s):
        """Dessine la silhouette de la lettre pour le stencil buffer."""
        glLineWidth(L_WIDTH * 2.0) 
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
        """Dessine un disque plein."""
        glBegin(GL_TRIANGLE_FAN)
        glColor4f(color[0], color[1], color[2], alpha)
        glVertex3f(0, 0, 0)
        for i in range(segments + 1):
            theta = 2.0 * math.pi * float(i) / float(segments)
            glVertex3f(radius * math.cos(theta), radius * math.sin(theta), 0)
        glEnd()

    @staticmethod
    def draw_circle_outline(radius, color, alpha=1.0, segments=32):
        """Dessine le contour du cercle."""
        glLineWidth(1.0)
        glBegin(GL_LINE_LOOP)
        glColor4f(color[0], color[1], color[2], alpha)
        for i in range(segments):
            theta = 2.0 * math.pi * float(i) / float(segments)
            glVertex3f(radius * math.cos(theta), radius * math.sin(theta), 0)
        glEnd()

    @staticmethod
    def draw_interactive_dot(pos, color, rot_inv, char=None):
        """Pastille avec Billboarding (toujours de face)."""
        radius = L_SIZE * 1.1 
        s_letter = radius * 0.55
        
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        glMultMatrixf(rot_inv)  # Annule la rotation pour le billboarding
        
        if char:
            # Pour les pastilles avec lettres : on utilise le stencil buffer
            # pour découper la lettre dans le cercle
            glEnable(GL_STENCIL_TEST)
            glStencilMask(0xFF) 
            glStencilFunc(GL_ALWAYS, 1, 0xFF)
            glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)
            glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)
            
            # Dessine la lettre dans le stencil buffer
            Gizmo.draw_letter_mask(char, s_letter)
            
            glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
            # On dessine le cercle partout SAUF là où la lettre a été dessinée
            glStencilFunc(GL_NOTEQUAL, 1, 0xFF) 
            glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP) 
            
            Gizmo.draw_filled_circle(radius, color, alpha=1.0)
            Gizmo.draw_circle_outline(radius, color, alpha=1.0)
            glDisable(GL_STENCIL_TEST)
        else:
            # Pastilles négatives : opaques et assombries pour bloquer ce qui est derrière
            dark_color = [c * 0.6 for c in color]
            Gizmo.draw_filled_circle(radius, dark_color, alpha=1.0)
            Gizmo.draw_circle_outline(radius, color, alpha=1.0)
            
        glPopMatrix()

    @staticmethod
    def render(width, height, model_view_matrix):
        """Affiche le Gizmo avec tri de profondeur manuel (Painter's Algorithm)."""
        # On extrait la rotation pure
        rot_only = np.copy(model_view_matrix)
        rot_only[3][0:3] = 0 
        rot_inv = np.copy(rot_only.T)
        
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        aspect = width / height
        # Volume ortho pour l'UI
        glOrtho(-aspect, aspect, -1, 1, -10, 10)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Positionnement dans le coin
        y_pos = G_TOP - 0.01
        x_pos = aspect - (G_RIGHT + 0.01) 
        glTranslatef(x_pos, y_pos, 0)
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # On désactive le Z-test car on va trier nous-mêmes
        glDisable(GL_DEPTH_TEST) 

        axis_len = 0.09 
        dot_radius = L_SIZE * 1.1
        dot_off = axis_len 
        
        # --- 1. DESSIN DES LIGNES ---
        # Dessinées en premier pour être toujours derrière les pastilles
        glPushMatrix()
        glMultMatrixf(rot_only)
        glLineWidth(2.5)
        glBegin(GL_LINES)
        glColor3f(*C_RED);   glVertex3f(0, 0, 0); glVertex3f(axis_len - dot_radius, 0, 0)
        glColor3f(*C_GREEN); glVertex3f(0, 0, 0); glVertex3f(0, axis_len - dot_radius, 0)
        glColor3f(*C_BLUE);  glVertex3f(0, 0, 0); glVertex3f(0, 0, axis_len - dot_radius)
        glEnd()
        glPopMatrix()

        # --- 2. TRI DES PASTILLES PAR PROFONDEUR ---
        dots = [
            ([dot_off, 0, 0], C_RED, 'X'),
            ([0, dot_off, 0], C_GREEN, 'Y'),
            ([0, 0, dot_off], C_BLUE, 'Z'),
            ([-dot_off, 0, 0], C_RED, None),
            ([0, -dot_off, 0], C_GREEN, None),
            ([0, 0, -dot_off], C_BLUE, None)
        ]

        def get_depth(dot_info):
            """Calcule la profondeur Z dans l'espace caméra."""
            pos = np.array(dot_info[0] + [1.0])
            transformed = rot_only @ pos
            # Retourne Z - les valeurs négatives sont devant, positives derrière
            return transformed[2]

        # Tri du plus profond (Z grand) au plus proche (Z petit)
        # Important : dessiner d'abord ce qui est derrière, puis ce qui est devant
        dots.sort(key=get_depth, reverse=True)

        # --- 3. DESSIN DES PASTILLES DANS L'ORDRE ---
        glPushMatrix()
        glMultMatrixf(rot_only)
        glClear(GL_STENCIL_BUFFER_BIT)
        for pos, color, char in dots:
            Gizmo.draw_interactive_dot(pos, color, rot_inv, char)
        glPopMatrix()

        # Restauration des états OpenGL
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)