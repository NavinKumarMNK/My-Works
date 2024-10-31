import requests
from pathlib import Path


def download_to_local(name: str, url: str, out_path: Path, parent_mkdir: bool = True):
    if not isinstance(out_path, Path):
        raise ValueError(f"{out_path} must be a valid pathlib.Path object")
    if parent_mkdir:
        out_path.mkdir(parents=True, exist_ok=True)

    try:
        response = requests.get(url)
        response.raise_for_status()
        (out_path / name).write_bytes(response.content)
        return True
    except requests.RequestException as e:
        print(f"failed to download {url}: {e}")
        return False
