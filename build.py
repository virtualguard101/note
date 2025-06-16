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

# except subprocess.CalledProcessError as e:
#     print(f"Process failed with {e.returncode}: {e.stderr}")

import subprocess
import sys
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    try:
        # Update recent notes at index
        logger.info("Refresh recent notes at index page...")
        result = subprocess.run(["uv", "run", "scripts/recent_notes.py"], 
                               check=True)
        logger.info("Refresh successfully!")
        
        # Get commit path & message
        path = input("Commit path: ").strip()
        if not path:
            raise ValueError("Choose at least a file to commit!")
            
        message = input("Commit message: ").strip()
        if not message:
            raise ValueError("Can't commit without message!")
            
        # Git operations
        logger.info(f"Add path: {path}")
        subprocess.run(["git", "add", f"{path}"], check=True)
        
        logger.info(f"Commit message: \"{message}\"")
        subprocess.run(["git", "commit", "-m", f"{message}"], check=True)
        
        logger.info("Push to origin/main...")
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        logger.info("Complete!")
        
    except KeyboardInterrupt:
        user = os.getlogin()
        logger.warning(f"Interrupted by {user}")
        return 1
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Proccess failed with {e.returncode}: {e.cmd}")
        if e.stdout:
            logger.info(f"OUT: {e.stdout}")
        if e.stderr:
            logger.error(f"ERROR: {e.stderr}")
            
    # Other errors...
        if "git push" in str(e.cmd):
            logger.info("Git push error!")
        elif "git add" in str(e.cmd):
            logger.info("Git add error!")
        
        return 2
        
    except ValueError as e:
        logger.error(f"Input error: {str(e)}")
        return 3
        
    except Exception as e:

        logger.exception(f"Other errors: {str(e)}")
        return 4
        
    return 0

if __name__ == "__main__":
    sys.exit(main())

