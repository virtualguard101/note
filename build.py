#!/usr/bin/env python3

import os

message = input("Commit message: ")

# git operation
os.system("git add .")
os.system(f"git commit -m \"{message}\"")
os.system("git push origin main")
