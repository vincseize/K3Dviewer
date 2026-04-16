# main.py
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QFrame, QWidget, QHBoxLayout, QPushButton, QLabel, QMenu, QAction, QMenuBar)
from PyQt5.QtGui import QSurfaceFormat, QFont, QColor, QIcon, QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import Qt, QPoint, QSize
from viewers.main_viewer import Viewer3D
from viewers.nav_controls import SideNavBar
from config.settings import APP_NAME, APP_COLOR_EXE, TOP_BT_NAV
from menus.svg_icons import SVG_ICONS

def load_stylesheet(filename):
    """Charge un fichier QSS et remplace les variables"""
    with open(filename, 'r') as f:
        stylesheet = f.read()
    # Remplacer les variables de couleur
    stylesheet = stylesheet.replace('#204060', APP_COLOR_EXE)
    return stylesheet

def create_app_icon(size=64): # Augmenté à 64 pour une meilleure qualité
    """Crée l'icône de l'application à partir du SVG"""
    renderer = QSvgRenderer(SVG_ICONS["favicon"].encode())
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    # Optionnel : améliorer le rendu
    painter.setRenderHint(QPainter.Antialiasing)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap), pixmap

class TitleBar(QWidget):
    """Barre de titre personnalisée avec boutons de contrôle"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(32)
        self.setStyleSheet(load_stylesheet('stylesheets/menuBar-stylesheet.qss'))
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 0, 0) # Marge réduite à gauche
        layout.setSpacing(0) # On gère l'espace manuellement
        
        # --- BLOC ICÔNE ---
        _, icon_pixmap = create_app_icon(64) 
        self.icon_label = QLabel()
        
        # On redimensionne l'image à 18px (un peu plus petit que les 20px du label)
        # Cela crée une "marge de sécurité" interne pour éviter la coupure
        scaled_icon = icon_pixmap.scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        self.icon_label.setPixmap(scaled_icon)
        # Le label est légèrement plus grand (24px) que l'image (18px)
        self.icon_label.setFixedSize(24, 32) 
        self.icon_label.setAlignment(Qt.AlignCenter) # CENTRE l'icône dans ses 24px
        
        layout.addWidget(self.icon_label)
        # ------------------

        # Titre de la fenêtre
        layout.addSpacing(5) # Espace entre icône et texte
        self.title_label = QLabel(APP_NAME)
        self.title_label.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.title_label)
        
        layout.addStretch()
        
        # Boutons de contrôle
        for btn_text, func, name in [
            ("─", self.parent.showMinimized, "min"),
            ("□", self.toggle_maximize, "max"),
            ("✕", self.parent.close, "close")
        ]:
            btn = QPushButton(btn_text)
            btn.setFixedSize(45, 32) # Standard Windows size (plus large pour cliquer)
            if name == "close": btn.setObjectName("close")
            btn.clicked.connect(func)
            if btn_text == "□": self.btn_maximize = btn
            layout.addWidget(btn)

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
        
        # Définir l'icône de la fenêtre (pour la barre des tâches)
        app_icon, _ = create_app_icon(64)
        self.setWindowIcon(app_icon)
        
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