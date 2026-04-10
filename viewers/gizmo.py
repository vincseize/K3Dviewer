# /viewers/gizmo.py

from OpenGL.GL import *
import numpy as np
from config.settings import *

class Gizmo:
    @staticmethod
    def draw_letter(char, pos, color):
        """Dessine une lettre en segments GL_LINES avec une taille réduite de 30%."""
        # Calcul de la taille réduite (30% plus petit que L_SIZE des settings)
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
            # Note: Dessiné sur le plan pour la profondeur
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
    def render(width, height, model_view_matrix):
        """Affiche le Gizmo (axes et lettres) en overlay 2D/3D."""
        # On extrait la rotation de la vue actuelle (on ignore la translation)
        rot_only = np.copy(model_view_matrix)
        rot_only[3][0:3] = 0 
        
        # Configuration de la projection Ortho pour le HUD (interface)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        aspect = width / height
        glOrtho(-aspect, aspect, -1, 1, -10, 10)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Positionnement du Gizmo dans le coin (Haut - Droite)
        glTranslatef(aspect - G_RIGHT, G_TOP, 0)
        glMultMatrixf(rot_only)
        
        # Désactivation du test de profondeur pour que le Gizmo soit toujours au-dessus
        glDisable(GL_DEPTH_TEST)
        glLineWidth(2.5)
        
        # Dessin des segments des axes
        axis_len = 0.06
        glBegin(GL_LINES)
        glColor3f(*C_RED);   glVertex3f(0, 0, 0); glVertex3f(axis_len, 0, 0)    # X
        glColor3f(*C_GREEN); glVertex3f(0, 0, 0); glVertex3f(0, 0, axis_len)    # Y
        glColor3f(*C_BLUE);  glVertex3f(0, 0, 0); glVertex3f(0, axis_len, 0)    # Z
        glEnd()
        
        # Dessin des étiquettes (Lettres)
        # Augmentation de l'éloignement (offset) par rapport à la pointe de l'axe
        letter_offset = axis_len + 0.05
        
        # X est sur l'axe X (Rouge)
        Gizmo.draw_letter('X', [letter_offset, 0, 0], C_RED)
        # Z est vertical (Bleu)
        Gizmo.draw_letter('Z', [0, letter_offset, 0], C_BLUE)
        # Y est en profondeur (Vert)
        Gizmo.draw_letter('Y', [0, 0, letter_offset], C_GREEN)
        
        # Restauration de l'état OpenGL
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)