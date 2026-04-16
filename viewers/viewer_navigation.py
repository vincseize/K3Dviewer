# viewers/viewer_navigation.py
import numpy as np
from config.settings import PAN_SPEED, ZOOM_SPEED, WHEEL_ZOOM_SPEED

class ViewerNavigation:
    def setup_nav_states(self):
        self.zoom_mode = False
        self.pan_mode = False
        self.is_panning = False
        self.is_zooming = False

    def handle_wheel_zoom(self, delta_y):
        self.zoom = np.clip(self.zoom + delta_y * WHEEL_ZOOM_SPEED, -30.0, -2.0)

    def compute_pan(self, dx, dy):
        # Utiliser la vitesse de pan depuis settings
        self.pan_x += dx * PAN_SPEED
        self.pan_y -= dy * PAN_SPEED

    def compute_rotation(self, dx, dy):
        self.rot_y += dx * 0.5
        self.rot_x += dy * 0.5