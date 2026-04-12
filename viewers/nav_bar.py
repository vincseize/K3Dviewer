from PyQt5.QtWidgets import QFrame, QVBoxLayout
from .nav_controls import NavButton

class SideNavBar(QFrame):
    """Barre latérale regroupant les outils de navigation"""
    def __init__(self, parent, viewer):
        super().__init__(parent)
        self.viewer = viewer
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)

        # Groupe 1: Modes d'interaction
        self.btn_zoom = NavButton("zoom", "Mode Zoom", True)
        self.btn_pan = NavButton("pan", "Mode Pan", True)
        
        layout.addWidget(self.btn_zoom)
        layout.addWidget(self.btn_pan)
        layout.addSpacing(15) 
        
        # Groupe 2: Affichage et Caméra
        self.btn_proj = NavButton("persp", "Perspective/Ortho", True, True, "ortho")
        self.btn_home = NavButton("home", "Reset View", False)
        self.btn_grid = NavButton("grid", "Grille", True)
        self.btn_grid.setChecked(True)
        self.btn_axes = NavButton("axes_on", "Axes", True, True, "axes_off")
        self.btn_axes.setChecked(True)

        layout.addWidget(self.btn_proj)
        layout.addWidget(self.btn_home)
        layout.addWidget(self.btn_grid)
        layout.addWidget(self.btn_axes)

        # Connexions vers le viewer
        self.btn_zoom.toggled.connect(self._toggle_zoom)
        self.btn_pan.toggled.connect(self._toggle_pan)
        self.btn_proj.toggled.connect(self.viewer.set_projection)
        self.btn_home.clicked.connect(self.viewer.reset_view)
        self.btn_grid.toggled.connect(self.viewer.set_grid_visible)
        self.btn_axes.toggled.connect(self.viewer.set_axes_visible)

    def uncheck_all_modes(self):
        """Désactive visuellement Zoom et Pan (utilisé pour le clic milieu)"""
        self.btn_zoom.blockSignals(True)
        self.btn_pan.blockSignals(True)
        self.btn_zoom.setChecked(False)
        self.btn_pan.setChecked(False)
        self.btn_zoom.blockSignals(False)
        self.btn_pan.blockSignals(False)

    def _toggle_zoom(self, checked):
        if checked:
            self.btn_pan.blockSignals(True)
            self.btn_pan.setChecked(False)
            self.btn_pan.blockSignals(False)
            self.viewer.activate_zoom_mode(True)
        else:
            self.viewer.activate_zoom_mode(False)

    def _toggle_pan(self, checked):
        if checked:
            self.btn_zoom.blockSignals(True)
            self.btn_zoom.setChecked(False)
            self.btn_zoom.blockSignals(False)
            self.viewer.activate_pan_mode(True)
        else:
            self.viewer.activate_pan_mode(False)

    def update_button_states(self):
        """Force l'état visuel selon les variables du viewer"""
        self.btn_zoom.blockSignals(True)
        self.btn_pan.blockSignals(True)
        self.btn_zoom.setChecked(self.viewer.zoom_mode)
        self.btn_pan.setChecked(self.viewer.pan_mode)
        self.btn_zoom.blockSignals(False)
        self.btn_pan.blockSignals(False)