import sys
from scripts.deduction import (
    fetch_deduction,
    check_deduction,
    load_progress,
    advance_gate
)

def main():
    gate, answer = fetch_deduction()
    progress = load_progress()
    current = progress["current_gate"]

    if current != "G3":
        print(f"Unexpected gate: {current}")
        return
    if gate in progress["completed"]:
        print(f"This deduction is already complete")
        return
    if "--dry-run" in sys.argv:
        if check_deduction(gate,answer,current,"SAILOR"):
            print("Yeh dry run hai, g4 would unlock")
        else:
            print("Yeh dry run hai, g4 would not unlock")
        return
    if advance_gate(progress, gate, answer, "SAILOR", "G4"):
        print("Deduction correct! Good work!")
    else:
        print("Not quite right. Reconsider the evidence.")
if __name__ == "__main__":
    main()