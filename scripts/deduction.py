import json
from pathlib import Path

def parse_deduction(text):
    parts = text.strip().split("=",1)

    if len(parts)!=2:
        raise ValueError("Expected a G1=ANSWER")
    gate = parts[0].upper().strip()
    answer = parts[1].strip().upper()

    if gate.startswith("G") == False or gate[1:].isdigit() == False:
        raise ValueError("Invalid Gate")

    if not answer:
        raise ValueError("Empty Answer")
    return gate,answer

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