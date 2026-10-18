import json
from pathlib import Path


def parse_deduction(text):
    text = text.strip()

    # A submission must contain exactly one deduction.
    if len(text.splitlines()) != 1:
        raise ValueError("Expected exactly one deduction")

    # There must be exactly one equals sign.
    if text.count("=") != 1:
        raise ValueError("Expected G1=ANSWER")

    gate, answer = text.split("=")

    gate = gate.strip().upper()
    answer = answer.strip().upper()

    if not gate.startswith("G") or not gate[1:].isdigit():
        raise ValueError("Invalid gate")

    if not answer:
        raise ValueError("Empty answer")

    return gate, answer

def fetch_deduction(path="deduction.txt"):
    text = Path(path).read_text(encoding="utf-8")
    return parse_deduction(text)

def check_deduction(gate, answer, expected_gate, expected_answer):
    if gate != expected_gate:
      return False
    if answer != expected_answer:
       return False
    return True

def load_progress():
    with open(".case/progress.json", "r") as f:
        return json.load(f)

def save_progress(progress):
    with open(".case/progress.json", "w") as f:
        json.dump(progress, f, indent=2)
def advance_gate(progress,gate,answer,expected_answer,next_gate):
    if gate != progress["current_gate"]:
        return False
    if gate in progress["completed"]:
        return False
    if not check_deduction(gate,answer,progress["current_gate"],expected_answer):
        return False
    progress["completed"].append(gate)
    progress["current_gate"] = next_gate
    save_progress(progress)
    return True