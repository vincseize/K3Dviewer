# config/settings.py
from datetime import datetime

PRINT_DEBUG = True  # Affiche les messages de debug dans la console

APP_NAME   = "K3D viewer"
VERSION    = "0.6.5"
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
PAN_SPEED = 0.008    # Vitesse du pan 
ZOOM_SPEED = 0.05    # Vitesse du zoom en mode drag
WHEEL_ZOOM_SPEED = 0.005  # Vitesse de la molette

# GRIDS AXES
GRID_SIZE = 10.0
GRID_SPACING = 0.2  # Espacement des lignes (0.2 = 50 lignes de chaque côté)
GRID_MAJOR_EVERY = 5  # Une ligne majeure toutes les 5 lignes
GRID_VISIBLE = True
GRID_COLOR_MINOR = (0.28, 0.28, 0.28, 0.15)  # Couleur lignes secondaires (RGBA)
GRID_COLOR_MAJOR = (0.28, 0.28, 0.28, 0.4)   # Couleur lignes principales (RGBA)
GRID_LINE_WIDTH_MINOR = 1.0
GRID_LINE_WIDTH_MAJOR = 1.5

# AXES
AXE_X_VISIBLE = True
AXE_Y_VISIBLE = False
AXE_Z_VISIBLE = True
AXE_LINE_WIDTH = 2.5