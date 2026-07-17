import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QTextEdit,
    QTreeWidget,
    QSplitter,
    QFrame,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.setWindowTitle("Correcteur Mathématique Mardown (CMM)")
        self.resize(800, 600)

    def initUI(self):
        # Create top-left and bottom frames with styled panel appearance
        topleft = QFrame()
        topleft.setFrameShape(QFrame.Shape.StyledPanel)
        bottom = QFrame()
        bottom.setFrameShape(QFrame.Shape.StyledPanel)
 
        # Create a text edit widget
        textedit = QTextEdit()
 
        # Create horizontal splitter to divide top area
        splitter1 = QSplitter(Qt.Orientation.Horizontal)
        splitter1.addWidget(topleft)
        splitter1.addWidget(textedit)
        # Set initial widget sizes
        splitter1.setSizes([100, 200])  
 
        # Create vertical splitter to divide left and bottom areas
        splitter2 = QSplitter(Qt.Orientation.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)
 
        # Create a central widget and layout to hold the splitters
        central_widget = QWidget()
        hbox = QHBoxLayout(central_widget)
        hbox.addWidget(splitter2)
        self.setCentralWidget(central_widget)
 
        # Apply cleanlooks style for visual consistency
        QApplication.setStyle("cleanlooks")
 
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("QSplitter")
        self.show()
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()