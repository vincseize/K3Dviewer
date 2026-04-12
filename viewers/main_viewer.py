import sys
import numpy as np
from PyQt5.QtWidgets import QOpenGLWidget, QApplication
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QPixmap, QPainter, QPen, QColor
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from config.settings import *
from .gizmo import Gizmo
from .menu_bar import MenuBar
from menus.context_menu import MainContextMenu

# Constante pour le décalage vertical des boutons
TOP_BT_NAV = 50

class Viewer3D(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.def_zoom = -12.0
        self.zoom = self.def_zoom
        self.pan_x, self.pan_y = 0.0, 0.0
        
        # Angles Turntable
        self.rot_x = 25.0
        self.rot_y = -45.0
        
        self.last_pos = QPoint()
        self.is_ortho = False
        self.show_grid = True
        self.show_axes = True
        self.context_menu = MainContextMenu(self)
        
        # États des modes
        self.zoom_mode = False
        self.is_zooming = False
        self.pan_mode = False
        self.is_panning = False
        
        # Créer des curseurs personnalisés
        self.zoom_cursor = self.create_zoom_cursor()
        self.pan_cursor = self.create_pan_cursor()

    # --- CURSEURS PERSONNALISÉS ---

    def create_zoom_cursor(self):
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(200, 200, 200), 2))
        painter.setBrush(QColor(60, 60, 60, 200))
        painter.drawEllipse(2, 2, 28, 28)
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        painter.drawLine(16, 8, 16, 24) # Verticale
        painter.drawLine(12, 12, 16, 8); painter.drawLine(20, 12, 16, 8) # Haut
        painter.drawLine(12, 20, 16, 24); painter.drawLine(20, 20, 16, 24) # Bas
        painter.end()
        return QCursor(pixmap, 16, 16)

    def create_pan_cursor(self):
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(200, 200, 200), 2))
        painter.setBrush(QColor(60, 60, 60, 200))
        painter.drawEllipse(2, 2, 28, 28)
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        painter.drawLine(8, 16, 24, 16); painter.drawLine(16, 8, 16, 24) # Croix
        painter.end()
        return QCursor(pixmap, 16, 16)

    # --- MODES D'INTERACTION (Appelés par SideNavBar) ---

    def activate_zoom_mode(self, checked):
        """Active/Désactive le mode zoom via argument booléen"""
        self.zoom_mode = checked
        if checked:
            self.pan_mode = False
            self.setCursor(self.zoom_cursor)
        else:
            self.is_zooming = False
            self.unsetCursor()

    def activate_pan_mode(self, checked):
        """Active/Désactive le mode pan via argument booléen"""
        self.pan_mode = checked
        if checked:
            self.zoom_mode = False
            self.setCursor(self.pan_cursor)
        else:
            self.is_panning = False
            self.unsetCursor()

    def _sync_navbar_ui(self):
        """Désactive visuellement les boutons si on change de mode manuellement"""
        # On remonte au parent (MainWindow) pour décocher les boutons
        root = self.window()
        if hasattr(root, 'nav_bar'):
            root.nav_bar.uncheck_all_modes()

    # --- MÉTHODES DE CONTRÔLE ---

    def set_projection(self, ortho_mode):
        self.is_ortho = ortho_mode
        self.makeCurrent()
        self.update_projection()
        self.update()

    def set_grid_visible(self, visible):
        self.show_grid = visible
        self.update()

    def set_axes_visible(self, visible):
        self.show_axes = visible
        self.update()

    def reset_view(self):
        self.zoom = self.def_zoom
        self.pan_x, self.pan_y = 0.0, 0.0
        self.rot_x, self.rot_y = 25.0, -45.0
        self.update_projection()
        self.update()

    # --- RENDU ---

    def update_projection(self):
        w, h = max(1, self.width()), max(1, self.height())
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / h
        if self.is_ortho:
            scale = abs(self.zoom) * 0.15
            glOrtho(-scale * aspect, scale * aspect, -scale, scale, 0.1, 1000.0)
        else:
            gluPerspective(45, aspect, 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(self.pan_x, self.pan_y, self.zoom)
        glRotatef(self.rot_x, 1, 0, 0)
        glRotatef(self.rot_y, 0, 1, 0)
        
        mv_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        if self.show_grid: self.draw_grid()
        self.draw_cube_centered()
        if self.show_axes: self.draw_world_axes()
        
        glDisable(GL_DEPTH_TEST)
        Gizmo.render(self.width(), self.height(), mv_matrix)
        cursor_pos = self.mapFromGlobal(QCursor.pos())
        MenuBar.render(self.width(), self.height(), cursor_pos.x(), self.height() - cursor_pos.y())
        glEnable(GL_DEPTH_TEST)

    def draw_grid(self):
        size = 10 * UNIT
        glBegin(GL_LINES)
        glColor4f(0.28, 0.28, 0.28, 0.3)
        for i in range(-10, 11):
            v = i * (size / 10)
            glVertex3f(-size, 0, v); glVertex3f(size, 0, v)
            glVertex3f(v, 0, -size); glVertex3f(v, 0, size)
        glEnd()

    def draw_world_axes(self):
        glLineWidth(2.0)
        glBegin(GL_LINES)
        glColor3f(*C_RED); glVertex3f(-10, 0, 0); glVertex3f(10, 0, 0)
        glColor3f(*C_BLUE); glVertex3f(0, 0, -10); glVertex3f(0, 0, 10)
        glEnd()

    def draw_cube_centered(self):
        s = UNIT
        glBegin(GL_LINES)
        glColor3f(0.8, 0.8, 0.8)
        # Simplifié pour l'exemple
        points = [(-s,-s,-s),(s,-s,-s),(s,s,-s),(-s,s,-s),(-s,-s,s),(s,-s,s),(s,s,s),(-s,s,s)]
        edges = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
        for e in edges:
            glVertex3fv(points[e[0]]); glVertex3fv(points[e[1]])
        glEnd()

    # --- EVENTS ---

    def wheelEvent(self, event):
        # On supprime self._sync_navbar_ui() pour garder les icônes actives
        delta = event.angleDelta().y()
        # Calcul du nouveau zoom avec limites
        self.zoom = np.clip(self.zoom + delta * 0.005, -30.0, -2.0)
        
        # Si on est en mode Ortho, il faut mettre à jour la matrice de projection
        self.update_projection()
        self.update()

    def mousePressEvent(self, event):
        self.last_pos = event.pos()
        
        # 1. Barre de menu (File, Edit, etc.)
        if MenuBar.handle_click(event.x(), self.height(), self.height()):
            self.update()
            return

        # 2. Mode Pan (Clic Gauche)
        if self.pan_mode and event.button() == Qt.LeftButton:
            self.is_panning = True
            self.pan_start_x, self.pan_start_y = event.x(), event.y()
            self.pan_start_pan_x, self.pan_start_pan_y = self.pan_x, self.pan_y
            
        # 3. Mode Zoom (Clic Gauche)
        elif self.zoom_mode and event.button() == Qt.LeftButton:
            self.is_zooming = True
            self.zoom_start_y, self.zoom_start_value = event.y(), self.zoom
            
        # 4. Clic Droit : Menu Contextuel (Garde l'icône bleue)
        elif event.button() == Qt.RightButton:
            self.context_menu.exec_(event.globalPos())
            
        # 5. Clic Milieu : Rotation
        elif event.button() == Qt.MidButton:
            # CONDITION : On ne synchronise (désactive) les icônes 
            # QUE SI on n'est pas déjà dans un mode actif.
            if not self.pan_mode and not self.zoom_mode:
                self._sync_navbar_ui()

    def mouseMoveEvent(self, event):
        if self.pan_mode and self.is_panning:
            factor = abs(self.zoom) * 0.001
            self.pan_x = self.pan_start_pan_x + (event.x() - self.pan_start_x) * factor
            self.pan_y = self.pan_start_pan_y - (event.y() - self.pan_start_y) * factor
            self.update()
        elif self.zoom_mode and self.is_zooming:
            delta_y = event.y() - self.zoom_start_y
            self.zoom = np.clip(self.zoom_start_value + (delta_y * 0.015), -30.0, -2.0)
            self.update_projection()
            self.update()
        elif event.buttons() & Qt.MidButton:
            diff = event.pos() - self.last_pos
            if QApplication.keyboardModifiers() & Qt.ShiftModifier:
                factor = abs(self.zoom) * 0.001
                self.pan_x += diff.x() * factor
                self.pan_y -= diff.y() * factor
            else:
                self.rot_y += diff.x() * 0.5
                self.rot_x += diff.y() * 0.5
            self.update()
        self.last_pos = event.pos()

    def mouseReleaseEvent(self, event):
        self.is_panning = False
        self.is_zooming = False

    def keyPressEvent(self, event):
        # Si on appuie sur ESC
        if event.key() == Qt.Key_Escape:
            # On vérifie si un mode est actif avant de reset
            if self.pan_mode or self.zoom_mode:
                # 1. On désactive les modes internes
                self.activate_pan_mode(False)
                self.activate_zoom_mode(False)
                
                # 2. On synchronise l'UI de la barre latérale
                self._sync_navbar_ui()
                
                # 3. On force un rafraîchissement visuel
                self.update()
        
        # Important : laisser passer les autres touches si nécessaire
        super().keyPressEvent(event)

    def initializeGL(self):
        glutInit()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(*C_BG)

    def resizeGL(self, w, h):
        self.update_projection()