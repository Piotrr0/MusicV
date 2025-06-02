from pathlib import Path

class DropFileHandler:
    def __init__(self):
        self.supported_formats = ['.mp3', '.wav']

    def handle_file(self, file_path: str) -> bool:
        suffix = Path(file_path).suffix.lower()
        return suffix in self.supported_formats