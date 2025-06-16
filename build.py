#!/usr/bin/env python3

import subprocess

# try:
#     os.system("uv run scripts/recent_notes.py")

#     path, message = input("Commit path: "), input("Commit message: ")

#     # git operation
#     os.system(f"git add {path}")
#     os.system(f"git commit -m \"{message}\"")
#     os.system("git push origin main")

# except KeyboardInterrupt as e:
#     print("User Interrupted", e)

try:
    # Update recent notes at index
    subprocess.run(["uv", "run", "scripts/recent_notes.py"])

    path, message = input("Commit path: "), input("Commit message: ")

    # Git operations
    subprocess.run(["git", "add", f"{path}"])
    subprocess.run(["git", "commit", "-m", f"\"{message}\""])
    subprocess.run(["git", "push", "origin", "main"])

except KeyboardInterrupt as e:
    print("User Interrupted", e)

except subprocess.CalledProcessError as e:
    print(f"Process failed with {e.returncode}: {e.stderr}")
