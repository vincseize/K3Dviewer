# menus/menu_bar.py
from PyQt5.QtWidgets import QMenu, QAction, QWidget, QMenuBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from utils.logger import debug_log

class MenuBarManager:
    """Gère la barre de menu de l'application"""
    
    def __init__(self, parent, viewer):
        self.parent = parent
        self.viewer = viewer
        self.menu_bar = None
        self.debug = False
        
    def setup_menu_bar(self):
        """Configure la barre de menu standard Qt avec Help à droite"""
        self.menu_bar = self.parent.menuBar()
        
        # --- MENUS DE GAUCHE ---
        fileMenu = QMenu("&File", self.parent)
        self.menu_bar.addMenu(fileMenu)
        
        self.newAction = QAction("&New", self.parent)
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.triggered.connect(self._on_new)
        fileMenu.addAction(self.newAction)
        
        self.openAction = QAction("&Open...", self.parent)
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self._on_open)
        fileMenu.addAction(self.openAction)
        
        self.saveAction = QAction("&Save", self.parent)
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self._on_save)
        fileMenu.addAction(self.saveAction)
        
        fileMenu.addSeparator()
        
        self.exitAction = QAction("E&xit", self.parent)
        self.exitAction.setShortcut("Ctrl+Q")
        self.exitAction.triggered.connect(self.parent.close)
        fileMenu.addAction(self.exitAction)
        
        # Menu Edit
        editMenu = QMenu("&Edit", self.parent)
        self.menu_bar.addMenu(editMenu)
        
        self.copyAction = QAction("&Copy", self.parent)
        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.triggered.connect(self._on_copy)
        editMenu.addAction(self.copyAction)
        
        self.pasteAction = QAction("&Paste", self.parent)
        self.pasteAction.setShortcut("Ctrl+V")
        self.pasteAction.triggered.connect(self._on_paste)
        editMenu.addAction(self.pasteAction)
        
        self.cutAction = QAction("Cu&t", self.parent)
        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.triggered.connect(self._on_cut)
        editMenu.addAction(self.cutAction)
        
        # Menu View
        viewMenu = QMenu("&View", self.parent)
        self.menu_bar.addMenu(viewMenu)
        
        self.gridAction = QAction("Show Grid", self.parent, checkable=True)
        self.gridAction.setChecked(self.viewer.show_grid)
        self.gridAction.triggered.connect(lambda checked: self.viewer.set_grid_visible(checked))
        viewMenu.addAction(self.gridAction)
        
        self.axesAction = QAction("Show Axes", self.parent, checkable=True)
        self.axesAction.setChecked(self.viewer.show_axes)
        self.axesAction.triggered.connect(lambda checked: self.viewer.set_axes_visible(checked))
        viewMenu.addAction(self.axesAction)
        
        viewMenu.addSeparator()
        
        self.resetViewAction = QAction("Reset View", self.parent)
        self.resetViewAction.setShortcut("Home")
        self.resetViewAction.triggered.connect(self.viewer.reset_view)
        viewMenu.addAction(self.resetViewAction)

        # --- MENU DE DROITE ---
        # On crée une barre de menu pour le coin droit
        self.right_menu_bar = QMenuBar()
        
        helpMenu = QMenu("&?", self.parent)
        self.right_menu_bar.addMenu(helpMenu)
        
        self.aboutAction = QAction("&About", self.parent)
        self.aboutAction.triggered.connect(self._on_about)
        helpMenu.addAction(self.aboutAction)
        
        self.aboutQtAction = QAction("About &Qt", self.parent)
        self.aboutQtAction.triggered.connect(self._on_about_qt)
        helpMenu.addAction(self.aboutQtAction)
        
        # On injecte cette barre dans le coin
        self.menu_bar.setCornerWidget(self.right_menu_bar, Qt.TopRightCorner)
        
        return self.menu_bar
    
    def _on_new(self): debug_log("MenuBar", "New action triggered")
    def _on_open(self): debug_log("MenuBar", "Open action triggered")
    def _on_save(self): debug_log("MenuBar", "Save action triggered")
    def _on_copy(self): debug_log("MenuBar", "Copy action triggered")
    def _on_paste(self): debug_log("MenuBar", "Paste action triggered")
    def _on_cut(self): debug_log("MenuBar", "Cut action triggered")
    
    def _on_about(self):
        from PyQt5.QtWidgets import QMessageBox
        from config.settings import APP_NAME, VERSION
        QMessageBox.about(self.parent, "About", f"{APP_NAME}\nVersion {VERSION}\n\n3D Viewer Application")
    
    def _on_about_qt(self):
        from PyQt5.QtWidgets import QApplication
        QApplication.aboutQt()