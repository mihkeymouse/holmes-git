
# Generate the playable git repo
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
DESTINATION = ROOT.parent / "Abbey-Grange-Case"

RECORDS = ["00_summons.md","01_hopkins.md","02_testimonies.md"]

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

    try:
        git(DESTINATION, "init","-b","main")

        readme = DESTINATION / "README.md"
        readme.write_text("Holmes-git\n\n"
                          "A Sherlock Holmes mystery played through Git \n\n"
                          "Begin the investigation with\n\n"

                          "git log --oneline\n"
                          "git show HEAD\n"
                          "git show HEAD~1\n\n"
                          "Examine the records under case/.\n")
        git(DESTINATION,"add","README.md")
        git(DESTINATION,
            "-c", "user.name=Dr.John Watson",
            "-c", "user.email=watson@fake.email",
            "commit","-m", "Watson opens the casebook")
        (DESTINATION / "case").mkdir()

        for record in RECORDS:
            source = ROOT/ "case"/ record
            target =  DESTINATION / "case" / record

            shutil.copyfile(source,target)

            git(DESTINATION, "add", "--", f"case/{record}")

            git(DESTINATION,
                "-c","user.name=Dr.John Watson",
                "-c", "user.email=watson@fake.email",
                "commit",
                "-m", f"Watson records {Path(record).stem}"
            )
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
