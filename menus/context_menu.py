# /menus/context_menu.py
from PyQt5.QtWidgets import QMenu, QAction

class MainContextMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Style sombre pour matcher avec le reste
        self.setStyleSheet("""
            QMenu {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #555555;
            }
            QMenu::item:selected {
                background-color: #444444;
            }
        """)

        # Ajout des menus "Fake"
        self.action1 = QAction("Menu 1", self)
        self.action2 = QAction("Menu 2", self)
        self.action3 = QAction("Menu 3", self)

        self.addActions([self.action1, self.action2, self.action3])
        self.addSeparator()
        
        # Un exemple d'action supplémentaire
        self.reset_view = QAction("Reset View", self)
        self.addAction(self.reset_view)