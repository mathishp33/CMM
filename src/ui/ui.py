import file_explorer

import sys
from pathlib import Path
import json

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QSplitter,
    QFrame,
    QTextBrowser,
    QFileDialog,
    QLineEdit,
)

def save_path_to_json(path):
    info_path = Path(__file__).parent.parent.parent / "resources" / "info.json"
    with open(info_path, "r") as f:
        data = json.load(f)

    data["root_dir"] = path

    with open(info_path, "w") as f:
        json.dump(data, f, indent=2)

def get_saved_path_from_json():
    info_path = Path(__file__).parent.parent.parent / "resources" / "info.json"
    with open(info_path, "r") as f:
        data = json.load(f)

    return data.get("root_dir", str(Path.home()))

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
        save_path_to_json(path)
        self.tree.set_root(path)
        self.path_edit.setText(path)

    def _root_changed(self, path):
        self.current_root = path
        save_path_to_json(path)
        self.path_edit.setText(path)

    def open_file(self, path):
        markdown = Path(path).read_text(encoding="utf-8")
        self.markdown_viewer.setMarkdown(markdown)

    def initFileExplorer(self):
        self.current_root = get_saved_path_from_json()
        if get_saved_path_from_json() == "":
            self.current_root = str(Path.home())

        self.path_edit = QLineEdit()
        self.path_edit.returnPressed.connect(self.goto_path)

        self.toolbar = self.addToolBar("Explorer")
        self.toolbar.addAction("↑", self.go_up)
        self.toolbar.addAction("📂", self.open_dir)
        self.toolbar.addWidget(self.path_edit)

        self.tree = file_explorer.CustomFileExplorer()
        self.tree.fileSelected.connect(self.open_file)
        self.tree.rootChanged.connect(self._root_changed)

        self.set_root(self.current_root)

    def initUI(self):
        self.initFileExplorer()

        bottom = QFrame()
        bottom.setFrameShape(QFrame.Shape.StyledPanel)
 
        # Create a markdown viewer using QTextBrowser
        self.markdown_viewer = QTextBrowser()
 
        # Create horizontal splitter to divide top area
        splitter1 = QSplitter(Qt.Horizontal)
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

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    app.exec()