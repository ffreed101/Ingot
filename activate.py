import os
import subprocess
import sys

def ensure_virtualenv():
    """Ensure the script is running in the virtual environment."""
    venv_python = os.path.join("venv", "Scripts", "python") if os.name == "nt" else os.path.join("venv", "bin", "python")
    
    # Check if the current Python interpreter matches the virtual environment's interpreter
    if sys.executable != os.path.abspath(venv_python):
        print("Re-running the script inside the virtual environment...")
        subprocess.run([venv_python, *sys.argv])
        sys.exit()

# Ensure the script runs inside the virtual environment
ensure_virtualenv()

# Your program starts here
print("Virtual environment is active!")
