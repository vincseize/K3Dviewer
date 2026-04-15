# viewers/viewer_navigation.py
import numpy as np

class ViewerNavigation:
    def setup_nav_states(self):
        self.zoom_mode = False
        self.pan_mode = False
        self.is_panning = False
        self.is_zooming = False

    def handle_wheel_zoom(self, delta_y):
        self.zoom = np.clip(self.zoom + delta_y * 0.005, -30.0, -2.0)

    def compute_pan(self, dx, dy):
        factor = abs(self.zoom) * 0.001
        self.pan_x += dx * factor
        self.pan_y -= dy * factor

    def compute_rotation(self, dx, dy):
        self.rot_y += dx * 0.5
        self.rot_x += dy * 0.5