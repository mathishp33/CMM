import sys
from pathlib import Path

from PySide6.QtCore import Qt, QDir
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTreeView,
    QWidget,
    QHBoxLayout,
    QTextEdit,
    QTreeWidget,
    QSplitter,
    QFrame,
    QFileSystemModel,
    QTextBrowser,
    QFileDialog,
    QLineEdit,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.setWindowTitle("Correcteur Mathématique Mardown (CMM)")
        self.resize(900, 650)

    def open_dir(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Ouvrir un dossier",
            str(Path.home())
        )

        if folder:
            self.set_root(folder)

    def goto_path(self):
        path = self.path_edit.text()

        if Path(path).exists():
            self.set_root(path)

    def go_up(self):
        parent = Path(self.current_root).parent

        if parent != Path(self.current_root):
            self.set_root(str(parent))

    def set_root(self, path):
        self.current_root = path

        index = self.model.setRootPath(path)
        self.tree.setRootIndex(index)
        self.path_edit.setText(path)

    def open_file(self, index):
        path = self.model.filePath(index)

        if path.endswith(".md"):
            markdown = Path(path).read_text(encoding="utf-8")
            self.markdown_viewer.setMarkdown(markdown)

    def initUI(self):
        #file system navigator
        top_left_f = QFrame()
        top_left_f.setFrameShape(QFrame.Shape.Panel)
        top_left_layout = QHBoxLayout(top_left_f)

        self.model = QFileSystemModel()
        self.model.setRootPath(str(Path.home()))
        self.model.setNameFilters(["*.md"])
        self.model.setNameFilterDisables(False)
        self.model.setFilter(QDir.AllDirs | QDir.Files | QDir.NoDotAndDotDot)

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(str(Path.home())))
        self.tree.hideColumn(1)
        self.tree.hideColumn(2)
        self.tree.hideColumn(3)
        self.tree.clicked.connect(self.open_file)

        self.current_root = str(Path.home())
        self.path_edit = QLineEdit()
        self.path_edit.returnPressed.connect(self.goto_path)

        self.toolbar = self.addToolBar("Explorer")

        self.toolbar.addAction("↑", self.go_up)
        self.toolbar.addAction("📂", self.open_dir)

        self.toolbar.addWidget(self.path_edit)

        top_left_layout.addWidget(self.tree)
        top_left_layout.addWidget(self.toolbar)

        bottom = QFrame()
        bottom.setFrameShape(QFrame.Shape.StyledPanel)
 
        # Create a markdown viewer using QTextBrowser
        self.markdown_viewer = QTextBrowser()
 
        # Create horizontal splitter to divide top area
        splitter1 = QSplitter(Qt.Orientation.Horizontal)
        splitter1.addWidget(self.tree)
        splitter1.addWidget(self.markdown_viewer)
        # Set initial widget sizes
        splitter1.setSizes([100, 200])
 
        # Create vertical splitter to divide left and bottom areas
        splitter2 = QSplitter(Qt.Orientation.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)
        splitter2.setSizes([100, 100])
 
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