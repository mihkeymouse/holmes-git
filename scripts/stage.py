import json
import os
from pathlib import Path
from urllib.request import urlopen

def load_stage(gate):
    stage_dir = Path(os.environ.get("CASE_STAGE_DIR", "stages"))

    if stage_dir.is_dir():
        config = json.loads(
            (stage_dir / f"{gate}.json").read_text(encoding="utf-8")
        )

        content = (stage_dir / f"{gate}.md").read_text(
            encoding="utf-8"
        )

    else:
        base_url = os.environ["CASE_STAGE_URL"].rstrip("/")

        with urlopen(f"{base_url}/{gate}.json") as response:
            config = json.load(response)

        with urlopen(f"{base_url}/{gate}.md") as response:
            content = response.read().decode("utf-8")

    config["content"] = content
    return config
