from pathlib import Path


def read_text(fpath: str) -> str:
    return Path(fpath).read_text(encoding="utf-8")

def write_text(fpath: Path, text: str) -> None:
    fpath.parent.mkdir(parents=True, exist_ok=True)
    fpath.write_text(text, encoding="utf-8")

