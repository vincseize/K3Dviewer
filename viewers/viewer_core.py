# viewers/viewer_core.py
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import Qt, QPoint
# Import centralisé des paramètres
from config.settings import (
    TOP_BT_NAV, 
    GRID_VISIBLE, 
    AXE_X_VISIBLE, 
    AXE_Y_VISIBLE, 
    AXE_Z_VISIBLE
)
from utils.logger import debug_log

class ViewerCore(QOpenGLWidget):
    """
    Cœur du viewer OpenGL gérant l'état de la caméra et les paramètres de base.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # --- CONFIGURATION DEBUG ---
        # Défini avant toute chose pour que les mixins (Rendering/Navigation) 
        # respectent ce réglage dès l'init.
        self.debug = False

        # --- ÉTAT DE LA CAMÉRA ---
        self.def_zoom = -12.0
        self.zoom = self.def_zoom
        self.pan_x, self.pan_y = 0.0, 0.0
        self.rot_x, self.rot_y = 25.0, -45.0
        
        # --- ÉTAT DU RENDU (Initialisé via settings.py) ---
        self.is_ortho = False
        self.show_grid = GRID_VISIBLE
        
        # On considère l'affichage global des axes actif si au moins l'un d'eux est visible
        self.show_axes = any([AXE_X_VISIBLE, AXE_Y_VISIBLE, AXE_Z_VISIBLE])
        
        # --- INTERACTION ---
        self.last_pos = QPoint()
        self.setFocusPolicy(Qt.StrongFocus)
        
        debug_log("ViewerCore", "Initialisation terminée", self.debug)

    def set_projection(self, ortho_mode):
        """Bascule entre perspective et orthographique"""
        debug_log("ViewerCore", f"Changement projection -> Ortho: {ortho_mode}", self.debug)
        self.is_ortho = ortho_mode
        self.makeCurrent()
        # Cette méthode est définie dans ViewerRendering (Mixin)
        if hasattr(self, 'update_projection'):
            self.update_projection()
        self.update()

    def set_grid_visible(self, visible):
        """Affiche ou masque la grille au sol"""
        debug_log("ViewerCore", f"Grille visible: {visible}", self.debug)
        self.show_grid = visible
        self.update()

    def set_axes_visible(self, visible):
        """Affiche ou masque les axes XYZ"""
        debug_log("ViewerCore", f"Axes visibles: {visible}", self.debug)
        self.show_axes = visible
        self.update()

    def reset_view(self):
        """Réinitialise la position et l'orientation de la caméra"""
        debug_log("ViewerCore", "Réinitialisation de la vue", self.debug)
        self.zoom = self.def_zoom
        self.pan_x, self.pan_y = 0.0, 0.0
        self.rot_x, self.rot_y = 25.0, -45.0
        
        if hasattr(self, 'update_projection'):
            self.update_projection()
        self.update()

    def get_view_state(self):
        """Retourne l'état actuel pour debug ou sauvegarde"""
        return {
            "zoom": self.zoom,
            "pan": (self.pan_x, self.pan_y),
            "rot": (self.rot_x, self.rot_y),
            "ortho": self.is_ortho
        }