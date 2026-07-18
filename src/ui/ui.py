from src.ui import file_explorer
from src.ui import worker
from src.core import config
from src.core import file_system

import sys
from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QSplitter,
    QFrame,
    QFileDialog,
    QLineEdit,
    QLabel,
    QPushButton,
    QGridLayout,
    QSpinBox
)

class MainWindow(QMainWindow):
    startCorrection = Signal(int, object)

    def __init__(self):
        super().__init__()
        self.initUI()

    def open_dir(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Ouvrir un dossier",
            str(Path.home())
        )

        if folder:
            self.set_workspace(folder)

    def goto_path(self):
        path = self.workspace_edit.text()

        if Path(path).exists():
            self.set_workspace(path)

    def go_up(self):
        parent = Path(self.current_workspace).parent

        if parent != Path(self.current_workspace):
            self.set_workspace(str(parent))

    def set_workspace(self, path):
        self.current_workspace = path
        file_system.save_to_json("dir", path)
        self.tree.set_workspace(path)
        self.workspace_edit.setText(path)

    def _workspace_changed(self, path):
        self.current_workspace = path
        file_system.save_to_json("dir", path)
        self.workspace_edit.setText(path)

    def open_file(self, path):
        name = Path(path).parent.name
        self.TD_name.setText(name)
        file_system.save_to_json("TD_name", name)

    def set_ex_nbr(self, value):
        file_system.save_to_json("ex_nbr", str(value))

    def correct_file(self):
        TD_dir = Path(self.current_workspace) / "TD"
        TD_corriges_dir = Path(self.current_workspace) / "TD corrigés"

        settings = config.Path_Settings(
            self.current_workspace,
            TD_dir,
            TD_corriges_dir,
            self.TD_name.text()
        )

        self.thread = QThread()
        self.worker = worker.CorrectionWorker()

        self.worker.moveToThread(self.thread)

        self.startCorrection.connect(self.worker.correct)

        self.worker.running.connect(self.get_thread_state)
        self.worker.log.connect(self.get_thread_log)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

        self.startCorrection.emit(self.ex_nbr.value(), settings)

    def get_thread_state(self, running):
        self.correct_button.setEnabled(not running)

    def get_thread_log(self, message):
        print(message)

    def initFileExplorer(self):
        self.current_workspace: str = file_system.get_from_json("dir", str(Path.home()))

        workspace_label = QLabel("Workspace: ")
        self.workspace_edit = QLineEdit()
        self.workspace_edit.returnPressed.connect(self.goto_path)

        self.toolbar = self.addToolBar("Explorer")
        self.toolbar.addAction("↑", self.go_up)
        self.toolbar.addAction("📂", self.open_dir)
        self.toolbar.addWidget(workspace_label)
        self.toolbar.addWidget(self.workspace_edit)

        self.tree = file_explorer.CustomFileExplorer()
        self.tree.fileSelected.connect(self.open_file)
        self.tree.workspaceChanged.connect(self._workspace_changed)

        self.set_workspace(self.current_workspace)

    def initUI(self):
        # file explorer
        self.initFileExplorer()

        # correction frame
        self.correction_frame = QFrame()
        self.correction_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.correction_layout = QGridLayout(self.correction_frame)
        self.correction_layout.setVerticalSpacing(5)
        self.correction_layout.setContentsMargins(5, 5, 5, 5)

        self.TD_name = QLineEdit(text = file_system.get_from_json("TD_name", ""))
        self.TD_name.setFixedWidth(200)
        self.ex_nbr = QSpinBox(value = int(file_system.get_from_json("ex_nbr", "1")))
        self.ex_nbr.valueChanged.connect(self.set_ex_nbr)
        self.ex_nbr.setFixedWidth(100)

        self.correct_button = QPushButton("Corriger")
        self.correct_button.clicked.connect(self.correct_file)
        self.correction_layout.addWidget(QLabel("Nom du TD: "), 0, 0, alignment = Qt.AlignRight)
        self.correction_layout.addWidget(self.TD_name, 0, 1, alignment = Qt.AlignLeft)
        self.correction_layout.addWidget(QLabel("N° de l'exercice: "), 1, 0, alignment = Qt.AlignRight)
        self.correction_layout.addWidget(self.ex_nbr, 1, 1, alignment = Qt.AlignLeft)

        self.correction_layout.addWidget(self.correct_button)

        # performance frame
        perf_frame = QFrame()
        perf_frame.setFrameShape(QFrame.Shape.StyledPanel)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.tree)
        splitter1.addWidget(self.correction_frame)
        splitter1.setSizes([250, 550])

        splitter2 = QSplitter(Qt.Orientation.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(perf_frame)
        splitter2.setSizes([350, 250])
 
        central_widget = QWidget()
        hbox = QHBoxLayout(central_widget)
        hbox.addWidget(splitter2)
        self.setCentralWidget(central_widget)
 
        QApplication.setStyle("cleanlooks")
 
        self.setGeometry(50, 50, 800, 600)
        self.setWindowTitle("CMM - Correcteur Mathématique Markdown")
        self.show()

def launch_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()