from pathlib import Path
import json

def read_text(fpath: str) -> str:
    return Path(fpath).read_text(encoding="utf-8")

def write_text(fpath: Path, text: str) -> None:
    fpath.parent.mkdir(parents=True, exist_ok=True)
    fpath.write_text(text, encoding="utf-8")

def save_to_json(key: str, item: any):
    info_path = Path(__file__).parent.parent.parent / "resources" / "info.json"
    with open(info_path, "r") as f:
        data = json.load(f)

    data[key] = item

    with open(info_path, "w") as f:
        json.dump(data, f, indent = 2)

def get_from_json(key: str, default: str) -> str:
    info_path = Path(__file__).parent.parent.parent / "resources" / "info.json"
    with open(info_path, "r") as f:
        data = json.load(f)

    return data.get(key, default)