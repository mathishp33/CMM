from pathlib import Path


class Settings:
    def __init__(self, model: str, temp: float):
        self.model = model
        self.temp = temp
        
        
class Path_Settings:
    def __init__(self, workspace: str, TD_dir: str, TD_corriges_dir: str, TD_name: str):
        self.update(workspace, TD_dir, TD_corriges_dir, TD_name)

    def get_input_fpath(self, ex_number: int) -> Path:
        return self.input_dir / rf"{self.TD_name}\Exercice {ex_number}.md"

    def get_output_fpath(self, ex_number: int) -> Path:
        return self.output_dir / rf"{self.TD_name}\Exercice {ex_number}.md"
    
    def update(self, workspace: str, TD_dir: str, TD_corriges_dir: str, TD_name: str):
        self.workspace = Path(workspace)
        self.input_dir = self.workspace / TD_dir
        self.output_dir = self.workspace / TD_corriges_dir
        self.TD_name = TD_name