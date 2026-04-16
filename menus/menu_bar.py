# menus/menu_bar.py
from PyQt5.QtWidgets import QMenu, QAction, QWidget, QMenuBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class MenuBarManager:
    """Gère la barre de menu de l'application"""
    
    def __init__(self, parent, viewer):
        self.parent = parent
        self.viewer = viewer
        self.menu_bar = None
        
    def setup_menu_bar(self):
        """Configure la barre de menu standard Qt"""
        self.menu_bar = self.parent.menuBar()
        
        # File menu
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
        
        # Edit menu
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
        
        # View menu
        viewMenu = QMenu("&View", self.parent)
        self.menu_bar.addMenu(viewMenu)
        
        self.gridAction = QAction("Show Grid", self.parent, checkable=True)
        self.gridAction.setChecked(self.viewer.show_grid)
        self.gridAction.triggered.connect(lambda: self.viewer.set_grid_visible(self.gridAction.isChecked()))
        viewMenu.addAction(self.gridAction)
        
        self.axesAction = QAction("Show Axes", self.parent, checkable=True)
        self.axesAction.setChecked(self.viewer.show_axes)
        self.axesAction.triggered.connect(lambda: self.viewer.set_axes_visible(self.axesAction.isChecked()))
        viewMenu.addAction(self.axesAction)
        
        viewMenu.addSeparator()
        
        self.projectionAction = QAction("Toggle Perspective/Ortho", self.parent)
        self.projectionAction.triggered.connect(lambda: self.viewer.set_projection(not self.viewer.is_ortho))
        viewMenu.addAction(self.projectionAction)
        
        viewMenu.addSeparator()
        
        self.resetViewAction = QAction("Reset View", self.parent)
        self.resetViewAction.setShortcut("Home")
        self.resetViewAction.triggered.connect(self.viewer.reset_view)
        viewMenu.addAction(self.resetViewAction)
        
        # Ajouter un espaceur extensible avant le menu "?"
        spacer = QWidget()
        spacer.setSizePolicy(QWidget().sizePolicy().Expanding, QWidget().sizePolicy().Preferred)
        self.menu_bar.setCornerWidget(spacer, Qt.TopRightCorner)
        
        # Menu "?" à droite
        helpMenu = QMenu("&?", self.parent)
        self.menu_bar.addMenu(helpMenu)
        
        self.aboutAction = QAction("&About", self.parent)
        self.aboutAction.triggered.connect(self._on_about)
        helpMenu.addAction(self.aboutAction)
        
        self.aboutQtAction = QAction("About &Qt", self.parent)
        self.aboutQtAction.triggered.connect(self._on_about_qt)
        helpMenu.addAction(self.aboutQtAction)
        
        return self.menu_bar
    
    def _on_new(self):
        """Nouveau fichier"""
        print("New action triggered")
        
    def _on_open(self):
        """Ouvrir un fichier"""
        print("Open action triggered")
        
    def _on_save(self):
        """Sauvegarder"""
        print("Save action triggered")
        
    def _on_copy(self):
        """Copier"""
        print("Copy action triggered")
        
    def _on_paste(self):
        """Coller"""
        print("Paste action triggered")
        
    def _on_cut(self):
        """Couper"""
        print("Cut action triggered")
        
    def _on_about(self):
        """À propos"""
        from PyQt5.QtWidgets import QMessageBox
        from config.settings import APP_NAME
        QMessageBox.about(self.parent, "About", f"{APP_NAME}\nVersion 1.0\n\n3D Viewer Application")
    
    def _on_about_qt(self):
        """À propos de Qt"""
        from PyQt5.QtWidgets import QApplication
        QApplication.aboutQt()