from PySide6.QtCore import QObject, QThread, Signal, Slot
import src.core.config as config
import src.core.file_system as file_system
import src.core.ollama_client as ollama_client
import src.core.prompts as prompts


class CorrectionWorker(QObject):
    running = Signal(bool)
    log = Signal(str)
    finished = Signal()

    def __init__(self):
        super().__init__()

    @Slot(int, object)
    def correct(self, ex_number, path_settings):
        self.running.emit(True)

        try:
            self.log.emit("Lecture du fichier ...")

            markdown = file_system.read_text(str(path_settings.get_input_fpath(ex_number)))

            self.log.emit("Correction en cours ...")

            correction = ollama_client.prompt_model(prompts.FINAL_PROMPT, markdown, model = "qwen3.5:9b")

            self.log.emit("Écriture de la correction ...")

            file_system.write_text(path_settings.get_output_fpath(ex_number), correction)

            self.log.emit("Terminé.")
        except Exception as e:
            self.log.emit(f"Erreur: {e}")
        finally:
            self.running.emit(False)
            self.finished.emit()