# /config/settings.py

# Unités et dimensions
import datetime
from datetime import datetime


APP_NAME  = "K3D viewer"
COPYRIGHT = "© 2025 " + str(datetime.now().year) + " - LRDS - All rights reserved."
DEVELOPERS = "LRDS - Vincseize - Karlova - C. POTTIER"
UNIT      = 1.0
G_SCALE   = 0.2
G_TOP     = 0.85
G_RIGHT   = 0.16
L_SIZE    = 0.02
L_WIDTH   = 1.5

# Couleurs Blender Style (RGB)
C_RED     = (1.0, 0.22, 0.26)  # X
C_GREEN   = (0.55, 0.85, 0.1)  # Y
C_BLUE    = (0.18, 0.52, 1.0)  # Z
C_GRID    = (0.28, 0.28, 0.28, 0.6)
C_BG      = (0.12, 0.12, 0.12, 1.0) # Fond sombre