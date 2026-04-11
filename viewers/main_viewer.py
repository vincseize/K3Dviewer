# viewers/main_viewer.py
import numpy as np
from PyQt5.QtWidgets import QOpenGLWidget, QApplication
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QPixmap, QPainter, QPen, QColor
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *  # IMPORTANT: Ajouter cet import
from config.settings import *
from .gizmo import Gizmo
from .menu_bar import MenuBar
from menus.context_menu import MainContextMenu

# Constante pour le décalage vertical des boutons (utilisée dans main.py)
TOP_BT_NAV = 50

class Viewer3D(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.def_zoom = -12.0
        self.zoom = self.def_zoom
        self.pan_x, self.pan_y = 0.0, 0.0
        
        # Angles Turntable (Blender Style)
        self.rot_x = 25.0
        self.rot_y = -45.0
        
        self.last_pos = QPoint()
        self.is_ortho = False
        self.show_grid = True
        self.show_axes = True
        self.context_menu = MainContextMenu(self)
        
        # État pour le zoom (mode toggle)
        self.zoom_mode = False
        self.zoom_start_y = 0
        self.zoom_start_value = 0.0
        self.is_zooming = False
        
        # État pour le pan (mode toggle)
        self.pan_mode = False
        self.pan_start_x = 0
        self.pan_start_y = 0
        self.pan_start_pan_x = 0.0
        self.pan_start_pan_y = 0.0
        self.is_panning = False
        
        # Créer des curseurs personnalisés
        self.zoom_cursor = self.create_zoom_cursor()
        self.pan_cursor = self.create_pan_cursor()

    def create_zoom_cursor(self):
        """Crée un curseur personnalisé pour le mode zoom."""
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Dessiner un cercle
        painter.setPen(QPen(QColor(200, 200, 200), 2))
        painter.setBrush(QColor(60, 60, 60, 200))
        painter.drawEllipse(2, 2, 28, 28)
        
        # Dessiner les flèches haut/bas
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        painter.drawLine(16, 8, 16, 20)
        painter.drawLine(12, 12, 16, 8)
        painter.drawLine(20, 12, 16, 8)
        painter.drawLine(16, 24, 16, 12)
        painter.drawLine(12, 20, 16, 24)
        painter.drawLine(20, 20, 16, 24)
        
        painter.end()
        
        return QCursor(pixmap, 16, 16)

    def create_pan_cursor(self):
        """Crée un curseur personnalisé pour le mode pan."""
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Dessiner un cercle
        painter.setPen(QPen(QColor(200, 200, 200), 2))
        painter.setBrush(QColor(60, 60, 60, 200))
        painter.drawEllipse(2, 2, 28, 28)
        
        # Dessiner les flèches 4 directions
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        # Flèche haut
        painter.drawLine(16, 8, 16, 18)
        painter.drawLine(12, 12, 16, 8)
        painter.drawLine(20, 12, 16, 8)
        # Flèche bas
        painter.drawLine(16, 24, 16, 14)
        painter.drawLine(12, 20, 16, 24)
        painter.drawLine(20, 20, 16, 24)
        # Flèche gauche
        painter.drawLine(8, 16, 18, 16)
        painter.drawLine(12, 12, 8, 16)
        painter.drawLine(12, 20, 8, 16)
        # Flèche droite
        painter.drawLine(24, 16, 14, 16)
        painter.drawLine(20, 12, 24, 16)
        painter.drawLine(20, 20, 24, 16)
        
        painter.end()
        
        return QCursor(pixmap, 16, 16)

    def activate_zoom_mode(self):
        """Active le mode zoom."""
        if self.pan_mode:
            self.deactivate_pan_mode()
        self.zoom_mode = True
        self.setCursor(self.zoom_cursor)
    
    def deactivate_zoom_mode(self):
        """Désactive le mode zoom."""
        if self.zoom_mode:
            self.zoom_mode = False
            self.is_zooming = False
            self.unsetCursor()

    def activate_pan_mode(self):
        """Active le mode pan."""
        if self.zoom_mode:
            self.deactivate_zoom_mode()
        self.pan_mode = True
        self.setCursor(self.pan_cursor)
    
    def deactivate_pan_mode(self):
        """Désactive le mode pan."""
        if self.pan_mode:
            self.pan_mode = False
            self.is_panning = False
            self.unsetCursor()

    # --- MÉTHODES DE CONTRÔLE ---

    def set_projection(self, ortho_mode):
        """Bascule entre Perspective (False) et Ortho (True)."""
        self.is_ortho = ortho_mode
        self.makeCurrent()
        self.update_projection()
        self.update()

    def set_grid_visible(self, visible):
        """Affiche/Masque la grille au sol."""
        self.show_grid = visible
        self.update()

    def set_axes_visible(self, visible):
        """Affiche/Masque les axes."""
        self.show_axes = visible
        self.update()

    def reset_view(self):
        """Action 'Home' : Réinitialise la caméra."""
        self.makeCurrent()
        self.zoom = self.def_zoom
        self.pan_x, self.pan_y = 0.0, 0.0
        self.rot_x = 25.0
        self.rot_y = -45.0
        self.update_projection()
        self.update()

    # --- LOGIQUE DE RENDU ---

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
        
        # Transformations de vue
        glTranslatef(self.pan_x, self.pan_y, self.zoom)
        glRotatef(self.rot_x, 1, 0, 0)
        glRotatef(self.rot_y, 0, 1, 0)
        
        mv_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        if self.show_grid: 
            self.draw_grid()
        
        # Cube avec DepthMask pour éviter le clignotement
        glDepthMask(GL_FALSE)
        self.draw_cube_centered()
        glDepthMask(GL_TRUE)
        
        if self.show_axes:
            self.draw_world_axes()
        
        # Gizmo 2D et Barre de menu
        glDisable(GL_DEPTH_TEST)
        Gizmo.render(self.width(), self.height(), mv_matrix)
        MenuBar.render(self.width(), self.height())

        # Passer la position de la souris pour les effets de survol
        cursor_pos = self.mapFromGlobal(QCursor.pos())
        MenuBar.render(self.width(), self.height(), cursor_pos.x(), self.height() - cursor_pos.y())

        glEnable(GL_DEPTH_TEST)

    def draw_grid(self):
        size = 10 * UNIT
        main_div, sub_div = 10, 50
        glLineWidth(1.0)
        glColor4f(0.28, 0.28, 0.28, 0.15)
        glBegin(GL_LINES)
        for i in range(-sub_div, sub_div + 1):
            if i % 5 == 0: continue
            v = i * (size / sub_div)
            glVertex3f(-size, 0, v)
            glVertex3f(size, 0, v)
            glVertex3f(v, 0, -size)
            glVertex3f(v, 0, size)
        glEnd()
        glLineWidth(1.5)
        glColor4f(0.28, 0.28, 0.28, 0.4)
        glBegin(GL_LINES)
        for i in range(-main_div, main_div + 1):
            if i == 0: continue
            v = i * (size / main_div)
            glVertex3f(-size, 0, v)
            glVertex3f(size, 0, v)
            glVertex3f(v, 0, -size)
            glVertex3f(v, 0, size)
        glEnd()

    def draw_world_axes(self):
        glLineWidth(2.5)
        glDepthRange(0.0, 0.999)
        glBegin(GL_LINES)
        glColor3f(*C_RED)
        glVertex3f(-10, 0, 0)
        glVertex3f(10, 0, 0)
        glColor3f(*C_BLUE)
        glVertex3f(0, 0, -10)
        glVertex3f(0, 0, 10)
        glEnd()
        glDepthRange(0.0, 1.0)

    def draw_cube_centered(self):
        glLineWidth(2.0)
        s = UNIT
        v = [
            [-s, -s, -s], [s, -s, -s], [s, s, -s], [-s, s, -s],
            [-s, -s, s], [s, -s, s], [s, s, s], [-s, s, s]
        ]
        e = [
            (0,1), (1,2), (2,3), (3,0),
            (4,5), (5,6), (6,7), (7,4),
            (0,4), (1,5), (2,6), (3,7)
        ]
        glBegin(GL_LINES)
        glColor3f(0.8, 0.8, 0.8)
        for edge in e:
            for vertex in edge:
                glVertex3fv(v[vertex])
        glEnd()

    # --- INPUTS ---

    def wheelEvent(self, event):
        # Fermer les menus ouverts
        from .menu_bar import MenuBar
        MenuBar.active_menu = None

        # Molette : zoom normal ET désactive tous les modes
        if self.zoom_mode:
            self.deactivate_zoom_mode()
            if hasattr(self.parent(), 'btn_zoom'):
                self.parent().btn_zoom.setChecked(False)
        if self.pan_mode:
            self.deactivate_pan_mode()
            if hasattr(self.parent(), 'btn_pan'):
                self.parent().btn_pan.setChecked(False)
        
        self.zoom += event.angleDelta().y() * 0.005
        if self.is_ortho: 
            self.update_projection()
        self.update()

    def mousePressEvent(self, event):
        self.last_pos = event.pos()
        
        # Mode Pan actif ET clic gauche
        if self.pan_mode and event.button() == Qt.LeftButton:
            self.is_panning = True
            self.pan_start_x = event.x()
            self.pan_start_y = event.y()
            self.pan_start_pan_x = self.pan_x
            self.pan_start_pan_y = self.pan_y
            event.accept()
            return
        
        # Mode Zoom actif ET clic gauche
        if self.zoom_mode and event.button() == Qt.LeftButton:
            self.is_zooming = True
            self.zoom_start_y = event.y()
            self.zoom_start_value = self.zoom
            event.accept()
            return
        
        # Clic droit : menu contextuel ET désactive tous les modes
        if event.button() == Qt.RightButton:
            if self.zoom_mode:
                self.deactivate_zoom_mode()
                if hasattr(self.parent(), 'btn_zoom'):
                    self.parent().btn_zoom.setChecked(False)
            if self.pan_mode:
                self.deactivate_pan_mode()
                if hasattr(self.parent(), 'btn_pan'):
                    self.parent().btn_pan.setChecked(False)
            self.context_menu.exec_(event.globalPos())
            event.accept()
            return
        
        # Clic milieu : rotation (désactive aussi les modes)
        if event.button() == Qt.MidButton:
            if self.zoom_mode:
                self.deactivate_zoom_mode()
                if hasattr(self.parent(), 'btn_zoom'):
                    self.parent().btn_zoom.setChecked(False)
            if self.pan_mode:
                self.deactivate_pan_mode()
                if hasattr(self.parent(), 'btn_pan'):
                    self.parent().btn_pan.setChecked(False)
            event.accept()
            return
        
        # Fermer les menus ouverts (sauf si clic sur la barre)
        from .menu_bar import MenuBar
    
        # Si clic droit ou milieu, fermer les menus
        if event.button() in (Qt.RightButton, Qt.MidButton):
            MenuBar.active_menu = None
        
        # Vérifier les clics sur la barre de menu (si pas déjà géré par MenuBar)
        if MenuBar.handle_click(event.x(), self.height(), self.height()):
            self.update()
            event.accept()
            return
        
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # Pan en mode drag
        if self.pan_mode and self.is_panning:
            delta_x = event.x() - self.pan_start_x
            delta_y = event.y() - self.pan_start_y
            factor = abs(self.zoom) * 0.001
            self.pan_x = self.pan_start_pan_x + (delta_x * factor)
            self.pan_y = self.pan_start_pan_y - (delta_y * factor)
            self.update()
            return
        
        # Zoom en mode drag
        if self.zoom_mode and self.is_zooming:
            delta_y = event.y() - self.zoom_start_y
            sensitivity = 0.01
            new_zoom = self.zoom_start_value + (delta_y * sensitivity)
            self.zoom = new_zoom
            
            if self.is_ortho:
                self.update_projection()
            self.update()
            return
        
        # Rotation et Pan au clic milieu
        diff = event.pos() - self.last_pos
        self.last_pos = event.pos()

        if event.buttons() & Qt.MidButton:
            if QApplication.keyboardModifiers() & Qt.ShiftModifier:
                # PANNING
                factor = abs(self.zoom) * 0.001
                self.pan_x += diff.x() * factor
                self.pan_y -= diff.y() * factor
            else:
                # ROTATION
                self.rot_y += diff.x() * 0.5
                self.rot_x += diff.y() * 0.5
            
            self.update()

    def mouseReleaseEvent(self, event):
        # Fin du drag pan
        if event.button() == Qt.LeftButton and self.is_panning:
            self.is_panning = False
            event.accept()
            return
        
        # Fin du drag zoom
        if event.button() == Qt.LeftButton and self.is_zooming:
            self.is_zooming = False
            event.accept()
            return
        
        super().mouseReleaseEvent(event)

    def resizeGL(self, w, h):
        self.update_projection()

    def initializeGL(self):
        # Initialiser GLUT (nécessaire pour le texte)
        glutInit(sys.argv)
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(*C_BG)