# main.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLabel, QMenuBar
from PyQt5.QtGui import QSurfaceFormat
from viewers.main_viewer import Viewer3D
from config.settings import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuration OpenGL
        fmt = QSurfaceFormat()
        fmt.setSamples(8)
        QSurfaceFormat.setDefaultFormat(fmt)
        
        # Central Widget (Le Viewer 3D)
        self.viewer = Viewer3D()
        self.setCentralWidget(self.viewer)
        self.setWindowTitle(APP_NAME)
        self.resize(1200, 800)

        # Création de la barre de menu
        self.init_menu_bar()

    def init_menu_bar(self):
        menubar = self.menuBar()
        
        # --- MENUS DE GAUCHE ---
        file_menu = menubar.addMenu('File')
        edit_menu = menubar.addMenu('Edit')
        render_menu = menubar.addMenu('Render')
        window_menu = menubar.addMenu('Window')

        # Exemple d'action pour tester
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # --- MENU D'AIDE A DROITE ---
        # Dans Qt, pour pousser un menu à droite, on crée une barre séparée 
        # ou un coin de widget (Corner Widget)
        self.help_menu = QMenuBar(menubar)
        help_action = self.help_menu.addMenu('?')
        
        # On ajoute le menu d'aide dans le coin droit de la barre principale
        menubar.setCornerWidget(self.help_menu)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())