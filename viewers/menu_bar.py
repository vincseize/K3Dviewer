# /viewers/menu_bar.py

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from config.settings import *

class MenuBar:
    @staticmethod
    def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_12):
        """Affiche du texte simple en coordonnées pixels."""
        glRasterPos2f(x, y)
        for char in text:
            glutBitmapCharacter(font, ord(char))

    @staticmethod
    def render(width, height):
        """Affiche la barre de menu en haut de la fenêtre."""
        # --- Configuration de la vue 2D (Overlay) ---
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, width, 0, height)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # --- 1. Arrière-plan de la barre (optionnel, gris sombre type Blender) ---
        bar_height = 24
        glColor4f(0.15, 0.15, 0.15, 1.0)
        glBegin(GL_QUADS)
        glVertex2f(0, height - bar_height)
        glVertex2f(width, height - bar_height)
        glVertex2f(width, height)
        glVertex2f(0, height)
        glEnd()

        # --- 2. Menu à GAUCHE ---
        glColor3f(0.9, 0.9, 0.9) # Texte presque blanc
        margin_x = 15
        text_y = height - 17 # Centrage vertical dans la barre
        
        # On définit les labels et on les espace
        menus = ["File", "Edit", "Render", "Window"]
        current_x = margin_x
        spacing = 50 # Espace entre les mots
        
        for label in menus:
            MenuBar.draw_text(current_x, text_y, label)
            current_x += spacing

        # --- 3. Aide à DROITE ---
        help_label = "?"
        help_margin_right = 20
        # On calcule la position en partant de la largeur totale
        MenuBar.draw_text(width - help_margin_right, text_y, help_label)

        # --- Restauration de l'état ---
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)