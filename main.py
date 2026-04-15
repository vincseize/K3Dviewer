# main.py
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QFrame, QWidget, QHBoxLayout, QPushButton, QLabel, QMenu, QAction, QMenuBar)
from PyQt5.QtGui import QSurfaceFormat, QFont, QColor
from PyQt5.QtCore import Qt, QPoint
from viewers.main_viewer import Viewer3D
from viewers.nav_controls import SideNavBar
from config.settings import APP_NAME, APP_COLOR_EXE, TOP_BT_NAV

def load_stylesheet(filename):
    """Charge un fichier QSS et remplace les variables"""
    with open(filename, 'r') as f:
        stylesheet = f.read()
    # Remplacer les variables de couleur
    stylesheet = stylesheet.replace('#204060', APP_COLOR_EXE)
    return stylesheet

class TitleBar(QWidget):
    """Barre de titre personnalisée avec boutons de contrôle"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(32)
        # Le style est maintenant chargé depuis le fichier externe
        self.setStyleSheet(load_stylesheet('stylesheets/menuBar-stylesheet.qss'))
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Titre de la fenêtre
        self.title_label = QLabel(APP_NAME)
        self.title_label.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.title_label)
        
        # Espace flexible
        layout.addStretch()
        
        # Bouton minimiser
        self.btn_minimize = QPushButton("─")
        self.btn_minimize.setFixedSize(30, 32)
        self.btn_minimize.clicked.connect(self.parent.showMinimized)
        layout.addWidget(self.btn_minimize)
        
        # Bouton maximiser/restaurer
        self.btn_maximize = QPushButton("□")
        self.btn_maximize.setFixedSize(30, 32)
        self.btn_maximize.clicked.connect(self.toggle_maximize)
        layout.addWidget(self.btn_maximize)
        
        # Bouton fermer
        self.btn_close = QPushButton("✕")
        self.btn_close.setObjectName("close")
        self.btn_close.setFixedSize(30, 32)
        self.btn_close.clicked.connect(self.parent.close)
        layout.addWidget(self.btn_close)
        
        # Variables pour le déplacement de la fenêtre
        self.drag_pos = None
        self.setMouseTracking(True)
    
    def toggle_maximize(self):
        """Bascule entre maximisé et normal"""
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.btn_maximize.setText("□")
        else:
            self.parent.showMaximized()
            self.btn_maximize.setText("❐")
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos()
            self.parent.drag_start_pos = self.parent.pos()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if self.drag_pos is not None:
            delta = event.globalPos() - self.drag_pos
            self.parent.move(self.parent.drag_start_pos + delta)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        self.drag_pos = None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Enlever la décoration de la fenêtre
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        fmt = QSurfaceFormat()
        fmt.setSamples(8)
        QSurfaceFormat.setDefaultFormat(fmt)
        
        # Widget central
        central_widget = QWidget()
        central_widget.setStyleSheet(f"background-color: {APP_COLOR_EXE};")
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)
        
        # Barre de titre personnalisée
        self.title_bar = TitleBar(self)
        central_layout.addWidget(self.title_bar)
        
        # Viewer 3D (créé avant la barre de menu)
        self.viewer = Viewer3D()
        
        # Barre de menu standard avec hauteur fixe
        self.setup_menu_bar()
        menu_bar = self.menuBar()
        menu_bar.setFixedHeight(28)
        central_layout.addWidget(menu_bar)
        
        # Ajouter le viewer après la barre de menu
        central_layout.addWidget(self.viewer)
        
        self.setCentralWidget(central_widget)
        
        # Barre de navigation latérale
        self.nav_bar = SideNavBar(self.viewer, self.viewer)
        
        self.setWindowTitle(APP_NAME)
        self.resize(1200, 800)
        
        # Variables pour le déplacement
        self.drag_start_pos = None

    def setup_menu_bar(self):
        """Configure la barre de menu standard Qt"""
        menuBar = self.menuBar()
        # Charger le style depuis le fichier externe
        menuBar.setStyleSheet(load_stylesheet('stylesheets/menuBar-stylesheet.qss'))
        
        # File menu
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        
        self.newAction = QAction("&New", self)
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.triggered.connect(self._on_new)
        fileMenu.addAction(self.newAction)
        
        self.openAction = QAction("&Open...", self)
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self._on_open)
        fileMenu.addAction(self.openAction)
        
        self.saveAction = QAction("&Save", self)
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self._on_save)
        fileMenu.addAction(self.saveAction)
        
        fileMenu.addSeparator()
        
        self.exitAction = QAction("E&xit", self)
        self.exitAction.setShortcut("Ctrl+Q")
        self.exitAction.triggered.connect(self.close)
        fileMenu.addAction(self.exitAction)
        
        # Edit menu
        editMenu = QMenu("&Edit", self)
        menuBar.addMenu(editMenu)
        
        self.copyAction = QAction("&Copy", self)
        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.triggered.connect(self._on_copy)
        editMenu.addAction(self.copyAction)
        
        self.pasteAction = QAction("&Paste", self)
        self.pasteAction.setShortcut("Ctrl+V")
        self.pasteAction.triggered.connect(self._on_paste)
        editMenu.addAction(self.pasteAction)
        
        self.cutAction = QAction("Cu&t", self)
        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.triggered.connect(self._on_cut)
        editMenu.addAction(self.cutAction)
        
        # View menu
        viewMenu = QMenu("&View", self)
        menuBar.addMenu(viewMenu)
        
        self.gridAction = QAction("Show Grid", self, checkable=True)
        self.gridAction.setChecked(self.viewer.show_grid)
        self.gridAction.triggered.connect(lambda: self.viewer.set_grid_visible(self.gridAction.isChecked()))
        viewMenu.addAction(self.gridAction)
        
        self.axesAction = QAction("Show Axes", self, checkable=True)
        self.axesAction.setChecked(self.viewer.show_axes)
        self.axesAction.triggered.connect(lambda: self.viewer.set_axes_visible(self.axesAction.isChecked()))
        viewMenu.addAction(self.axesAction)
        
        viewMenu.addSeparator()
        
        self.projectionAction = QAction("Toggle Perspective/Ortho", self)
        self.projectionAction.triggered.connect(lambda: self.viewer.set_projection(not self.viewer.is_ortho))
        viewMenu.addAction(self.projectionAction)
        
        viewMenu.addSeparator()
        
        self.resetViewAction = QAction("Reset View", self)
        self.resetViewAction.setShortcut("Home")
        self.resetViewAction.triggered.connect(self.viewer.reset_view)
        viewMenu.addAction(self.resetViewAction)
        
        # Ajouter un espaceur extensible avant le menu "?"
        spacer = QWidget()
        spacer.setSizePolicy(QWidget().sizePolicy().Expanding, QWidget().sizePolicy().Preferred)
        menuBar.setCornerWidget(spacer, Qt.TopRightCorner)
        
        # Menu "?" à droite
        helpMenu = QMenu("&?", self)
        menuBar.addMenu(helpMenu)
        
        self.aboutAction = QAction("&About", self)
        self.aboutAction.triggered.connect(self._on_about)
        helpMenu.addAction(self.aboutAction)
        
        self.aboutQtAction = QAction("About &Qt", self)
        self.aboutQtAction.triggered.connect(QApplication.aboutQt)
        helpMenu.addAction(self.aboutQtAction)
    
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
        QMessageBox.about(self, "About", f"{APP_NAME}\nVersion 1.0\n\n3D Viewer Application")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Positionner la barre de navigation latérale (32px title + 28px menu = 60px)
        self.nav_bar.setGeometry(self.width() - 45, 60 + TOP_BT_NAV, 40, 270)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())