# config/settings.py
from datetime import datetime

APP_NAME   = "K3D viewer"
VERSION    = "0.5.0"
COPYRIGHT  = f"© 2025 - {datetime.now().year} - LRDS - All rights reserved."
DEVELOPERS = "LRDS - Vincseize - Karlova - C. POTTIER"
APP_COLOR_EXE   = "#204060"

UNIT       = 1.0
G_SCALE    = 0.2
G_TOP      = 0.85
G_RIGHT    = 0.16
L_SIZE     = 0.02
L_WIDTH    = 1.5
TOP_BT_NAV = 120

# Couleurs Blender Style (RGB)
C_RED      = (1.0, 0.22, 0.26)  # X
C_GREEN    = (0.55, 0.85, 0.1)  # Y
C_BLUE     = (0.18, 0.52, 1.0)  # Z
C_GRID     = (0.28, 0.28, 0.28, 0.6)
C_BG       = (0.12, 0.12, 0.12, 1.0)

# Vitesse de navigation
PAN_SPEED = 0.002    # Vitesse du pan (défaut: 0.002)
ZOOM_SPEED = 0.05    # Vitesse du zoom en mode drag (défaut: 0.05)
WHEEL_ZOOM_SPEED = 0.005  # Vitesse de la molette