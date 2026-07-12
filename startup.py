import subprocess
import sys
import os

def main():
    print(" Running data preparation...")
    try:
        # Run data_prep.py to generate the joblib files
        subprocess.run([sys.executable, "data_prep.py"], check=True)
        print(" Data preparation complete!")
    except Exception as e:
        print(f" Data preparation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
