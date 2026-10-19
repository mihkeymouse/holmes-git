
import json
import os
from pathlib import Path
from urllib.request import urlopen

def load_stage(gate, outcome=None):
    stage_dir = Path(os.environ.get("CASE_STAGE_DIR","stages"))
    local = stage_dir.is_dir()

    if local:
        config = json.loads((stage_dir / f"{gate}.json").read_text(encoding="utf-8"))
    else:
        base_url = os.environ["CASE_STAGE_URL"].rstrip("/")
        with urlopen(f"{base_url}/{gate}.json") as response:
            config = json.load(response)

    #G5 has 2 outcomes
    if outcome is not None:
        config.update(config["outcomes"][outcome])

    #G0: load the opening records
    if "opening_records" in config:
        records = []

        for filename in config["opening_records"]:
            if local:
                content = (stage_dir.parent / filename).read_text(
                    encoding="utf-8"
                )
            else:
                root_url = base_url.rsplit("/", 1)[0]
                with urlopen(f"{root_url}/{filename}") as response:
                    content = response.read().decode("utf-8")

            records.append((filename, content))

        config["opening_contents"] = records
        return config

    source = config.get("source", f"{gate}.md")

    if local:
        content = (stage_dir / source).read_text(encoding="utf-8")
    else:
        with urlopen(f"{base_url}/{source}") as response:
            content = response.read().decode("utf-8")

    config["content"] = content
    return config
