import src.core.config as config
import src.core.file_system as file_system
import src.core.ollama_client as ollama_client
import src.core.prompts as prompts

class Correction:
    def __init__(self, path_settings: config.Path_Settings):
        self.path_settings = path_settings

    def correct(self, ex_number: int) -> None:
        markdown_content = file_system.read_text(str(self.path_settings.get_input_fpath(ex_number)))

        current_correction = ollama_client.prompt_model(prompts.FINAL_PROMPT, markdown_content, model="qwen3.5:9b")

        file_system.write_text(self.path_settings.get_output_fpath(ex_number), current_correction)