import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QSurfaceFormat
from viewers.main_viewer import Viewer3D
from config.settings import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        fmt = QSurfaceFormat()
        fmt.setSamples(8)
        QSurfaceFormat.setDefaultFormat(fmt)
        
        self.viewer = Viewer3D()
        self.setCentralWidget(self.viewer)
        self.setWindowTitle(APP_NAME)
        self.resize(1200, 800)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())