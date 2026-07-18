from pathlib import Path

from PySide6.QtCore import QDir, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTreeView,
    QFileSystemModel,
)


class CustomFileExplorer(QWidget):
    fileSelected = Signal(str)
    workspaceChanged = Signal(str)

    def __init__(self):
        super().__init__()

        self.model = QFileSystemModel(self)
        self.model.setRootPath(str(Path.home()))
        self.model.setNameFilters(["*.md"])
        self.model.setNameFilterDisables(False)
        self.model.setFilter(QDir.AllDirs | QDir.Files | QDir.NoDotAndDotDot)

        self.tree = QTreeView(self)
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(str(Path.home())))
        self.tree.hideColumn(1)
        self.tree.hideColumn(2)
        self.tree.hideColumn(3)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tree)

        self.tree.clicked.connect(self._item_clicked)
        self.tree.doubleClicked.connect(self._double_clicked)

    def _double_clicked(self, index):
        if self.model.isDir(index):
            self.set_workspace(self.model.filePath(index))

    def _item_clicked(self, index):
        path = self.model.filePath(index)
        if path.endswith(".md"):
            self.fileSelected.emit(path)

    def set_workspace(self, path):
        index = self.model.setRootPath(path)
        self.tree.setRootIndex(index)
        self.workspaceChanged.emit(path)

    def workspace_path(self):
        return self.model.rootPath()