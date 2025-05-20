#!/usr/bin/env python3

import os

try:
    path, message = input("Commit path: "), input("Commit message: ")

    # git operation
    os.system(f"git add {path}")
    os.system(f"git commit -m \"{message}\"")
    os.system("git push origin main")

except KeyboardInterrupt as e:
    print("User Interrupted", e)
