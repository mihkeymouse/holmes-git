import json
import sys
import os
from copy import deepcopy
from pathlib import Path
from scripts.deduction import (
    fetch_deduction,
    check_deduction,
    load_progress,
    save_progress,
    advance_gate,
)
from scripts.watson import commit_record
from scripts.stage import load_stage


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    # Read submitted deduction
    try:
        gate, answer = fetch_deduction()
        progress = load_progress()
    except Exception as e:
        print(f"Error: {e}")
        return 1

    current = progress["current_gate"]

    # Reject outdated or premature deductions
    if gate != current:
        print(
            f"Unexpected deduction for gate {gate}. "
            f"Current gate is {current}."
        )
        return 1

    # Prevent completed gates from repeating
    if gate in progress["completed"]:
        print(f"Gate {gate} has already been completed.")
        return 1

    #LOAD DEDUCTION + NEXT PASSAGE
    try:
        config = load_stage(current)
    except Exception as e:
        print(f"could not load stage {current}: {e}")
        return 1
    

    # Check answer
    valid = check_deduction(
        gate, answer, current, config["answer"]
    )

    # Dry runs
    if "--dry-run" in argv:
        if valid:
            print(
                f"Yeh dry run hai: "
                f"{config['next_gate']} would be unlocked."
            )
            return 0

        print("Dry run: Deduction is invalid.")
        return 1

    if not valid:
        print("Deduction is invalid.")
        return 1

    # Don't overwrite existing record
    chapter = Path(config["chapter"])

    if chapter.exists():
        print(
            f"Chapter {chapter} already exists. "
            "Aborting to prevent overwrite."
        )
        return 1

    original_progress = deepcopy(progress)
    original_readme = None

    try:
        # Make the next Watson record
        chapter.parent.mkdir(parents=True, exist_ok=True)

        chapter.write_text(
            config["content"],
            encoding="utf-8"
        )

        # Advance the gate and save progress
        advanced = advance_gate(
            progress,
            gate,
            answer,
            config["answer"],
            config["next_gate"]
        )

        if not advanced:
            raise RuntimeError("Gate advancement failed")

        # Commit new record + progress
        readme = Path("README.md")
        original_readme = readme.read_text(encoding="utf-8")
        start = "<!--DEDUCTION_START-->"
        end = "<!--DEDUCTION_END-->"
        before, rest = original_readme.split(start,1)
        old_prompt, after = rest.split(end,1)

        new_readme = (before + start + "\n" + config["next_prompt"].strip()+"\n" + end + after)
        readme.write_text(new_readme,encoding="utf-8")
        commit_record(str(chapter))
    except Exception as e:

        # Try a rollback
        try:
            save_progress(original_progress)
        except Exception as rollback_error:
            print(f"Rollback failed: {rollback_error}")

        chapter.unlink(missing_ok=True)
        if original_readme != None:
            Path("README.md").write_text(original_readme,encoding="utf-8")
            

        print(f"Error during gate advancement: {e}")
        return 1

    print(
        f"Deduction accepted. "
        f"{config['next_gate']} unlocked."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
