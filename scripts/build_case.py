
# Generate the playable git repo
from pathlib import Path
import shutil
import subprocess
import sys
import json

ROOT = Path(__file__).resolve().parent.parent
DESTINATION = ROOT.parent / "The-Adventure-of-the-Abbey_Grange"

RECORDS = ["00_summons.md","01_hopkins.md","02_testimonies.md","03_dining_room.md"]
def git(directory, *args):
    subprocess.run(["git", *args], cwd=directory, check=True)

def build():
    if DESTINATION.exists():
        raise FileExistsError(f"DESTINATION ALREADY EXISTS: {DESTINATION}")
    for record in RECORDS:
        source = ROOT/"case"/record

        if source.is_file() == False:
            raise FileNotFoundError(f"Missing record {source}")
    DESTINATION.mkdir()
    shutil.copyfile(ROOT / ".gitignore", DESTINATION / ".gitignore")

    try:
        git(DESTINATION, "init","-b","main")

        readme = DESTINATION / "README.md"
        
        readme.write_text(
            "# The Adventure of the Abbey Grange\n\n"
            "*A Sherlock Holmes mystery played through Git.*\n\n"

            "You are Sherlock Holmes. Dr. Watson has kept a "
            "version-controlled record of a quite remarkable case.\n\n"

            "Investigate the evidence, follow the history and draw your deductions.\n\n"

            "## How to Play\n\n"
            "Explore Watson's records, commits and branches using:\n\n"
            "```bash\n"
            "git log --all --oneline --graph\n"
            "git branch -a\n"
            "git show HEAD\n"
            "```\n\n"

            "New case-files will appear under `case/` as "
            "the investigation advances.\n\n"

            "Write your answer in `deduction.txt`, then commit "
            "and push it.\n\n"
            "Once GitHub Actions completes, retrieve "
            "the latest records using:\n\n"
            "```bash\n"
            "git pull --rebase\n"
            "```\n\n"

            "## Begin the Investigation\n\n"
            "Open `deduction.txt` and enter:\n\n"
            "```text\n"
            "G0=START!\n"
            "```\n\n"

            "Then run:\n\n"
            "```bash\n"
            "git add deduction.txt\n"
            "git commit -m \"START!\"\n"
            "git push\n"
            "```\n\n"

        
            "**The game is afoot!**\n",
            encoding="utf-8"
        )


      
        (DESTINATION / "case").mkdir()
        (DESTINATION / ".case").mkdir()

        progress = {"current_gate": "G0", "completed":[]}
        (DESTINATION / ".case" / "progress.json").write_text(json.dumps(progress, indent=2))
        (DESTINATION / "deduction.txt").write_text("G0=\n")

        (DESTINATION / "scripts").mkdir()

        for script in ["advance.py","deduction.py", "watson.py","stage.py"]:
            shutil.copyfile(ROOT / "scripts" / script, DESTINATION / "scripts" / script)
        (DESTINATION / ".github" / "workflows").mkdir(parents=True)
        shutil.copyfile(ROOT /".github"/ "workflows" / "deduction.yml", DESTINATION / ".github" / "workflows" / 'deduction.yml')
        git(DESTINATION,"add","README.md", ".case/progress.json", "deduction.txt", "scripts/", ".github/",".gitignore")
        git(DESTINATION,
            "-c", "user.name=Dr.John Watson",
            "-c", "user.email=watson@fake.email",
            "commit","-m", "Watson opens the casebook")

        
    except Exception:
        shutil.rmtree(DESTINATION)
        raise
    print(f"Playable repo created: {DESTINATION}")

if __name__ == "__main__":
    try:
        build()
    except (
        FileExistsError,
        FileNotFoundError,
        subprocess.CalledProcessError
       ) as error:
        print(f"Build failed: {error}",file=sys.stderr)
        sys.exit(1)
        