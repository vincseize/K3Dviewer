# utils/logger.py
from config.settings import PRINT_DEBUG

def debug_log(module_name, message, local_debug=False):
    """
    Centralise la logique de debug.
    PRINT_DEBUG (global) doit être True.
    local_debug (spécifique au fichier) doit être True.
    """
    if PRINT_DEBUG and local_debug:
        print(f"[DEBUG][{module_name}] {message}")