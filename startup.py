import subprocess
import sys
import os

def main():
    print("Starting data preparation...")
    
    # Check if data files already exist
    if os.path.exists("recipe_data.joblib"):
        print(" Data files already exist. Skipping preparation.")
        return
    
    try:
        # Run data_prep.py to generate the joblib files
        result = subprocess.run(
            [sys.executable, "data_prep.py"], 
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr)
        print(" Data preparation complete!")
    except subprocess.CalledProcessError as e:
        print(f"Data preparation failed with error: {e}")
        print(e.stdout)
        print(e.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
