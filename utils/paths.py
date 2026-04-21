# utils/paths.py
import os
import sys

def get_resource_path(relative_path):
    """ Récupère le chemin absolu vers la ressource, compatible PyInstaller """
    try:
        # PyInstaller crée un dossier temporaire dans _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)