import subprocess
from pathlib import Path

def commit_record(filename):
    path = Path(filename)
    progress = Path(".case/progress.json")
    if not progress.is_file():
        raise FileNotFoundError(filename)
    if path.is_file() == False:
        raise FileNotFoundError(filename)

    subprocess.run(["git","add","--",str(path), str(progress)], check=True)
    subprocess.run(["git","-c", "user.name=Dr. John Watson", "-c", "user.email=watson@fakeemail.com",
                    "commit", "-m", f"Watson records {path.stem}",
                    "--", str(path), str(progress)], check=True)
    

if __name__ == "__main__":
    commit_record("case/02_test.md")