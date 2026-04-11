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
        if width == 0 or height == 0:
            return
            
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

        # --- 1. Arrière-plan de la barre ---
        bar_height = 28
        glColor4f(0.18, 0.18, 0.18, 1.0)  # Gris foncé type Blender
        glBegin(GL_QUADS)
        glVertex2f(0, height - bar_height)
        glVertex2f(width, height - bar_height)
        glVertex2f(width, height)
        glVertex2f(0, height)
        glEnd()

        # --- 2. Ligne de séparation en bas de la barre ---
        glColor4f(0.3, 0.3, 0.3, 1.0)
        glLineWidth(1.0)
        glBegin(GL_LINES)
        glVertex2f(0, height - bar_height)
        glVertex2f(width, height - bar_height)
        glEnd()

        # --- 3. Menu à GAUCHE ---
        glColor3f(0.85, 0.85, 0.85)  # Texte gris clair
        margin_x = 12
        text_y = height - 20  # Centrage vertical dans la barre (28px de haut)
        
        # Labels du menu
        menus = ["File", "Edit", "View", "Render", "Window", "Help"]
        current_x = margin_x
        spacing = 45  # Espace entre les mots
        
        for label in menus:
            MenuBar.draw_text(current_x, text_y, label)
            current_x += spacing

        # --- 4. Informations supplémentaires à DROITE ---
        # Version de l'application
        version_text = f"{APP_NAME} v1.0"
        version_width = len(version_text) * 7  # Approximation largeur texte
        right_margin = 80
        MenuBar.draw_text(width - right_margin, text_y, version_text)
        
        # Stats (optionnel)
        # stats_text = "FPS: 60"
        # MenuBar.draw_text(width - 25, text_y, stats_text)

        # --- 5. Surbrillance au survol (à implémenter avec détection de souris) ---
        # Pour l'instant, simple affichage
        
        # --- Restauration de l'état ---
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)