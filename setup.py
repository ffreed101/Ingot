import os
import subprocess
import sys
from pathlib import Path

def create_virtualenv():
    """Create a virtual environment."""
    print("Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    print("Virtual environment created in the 'venv' folder.")

def update_pip(venv_python):
    """Update pip to the latest version."""
    print("Checking if pip needs to be updated...")
    subprocess.run([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"], check=True)
    print("pip has been updated to the latest version.")

def install_dependencies():
    """Install dependencies using pip."""
    print("Installing dependencies...")

    # Use pathlib to construct paths dynamically
    venv_path = Path("venv")
    if os.name == "nt":  # Windows
        venv_python = venv_path / "Scripts" / "python.exe"
    else:  # macOS/Linux
        venv_python = venv_path / "bin" / "python"

    # Update pip before installing dependencies
    update_pip(venv_python)

    # Get the path to requirements.txt relative to the script's location
    requirements_path = Path(__file__).parent / "requirements.txt"

    # Ensure requirements.txt exists
    if not requirements_path.exists():
        raise FileNotFoundError(f"Could not find 'requirements.txt' at {requirements_path}")

    # Use the virtual environment's Python to install dependencies
    subprocess.run([str(venv_python), "-m", "pip", "install", "-r", str(requirements_path)], check=True)
    print("Dependencies installed!")

def main():
    """Main function to orchestrate the setup."""
    print("Starting setup process...")
    create_virtualenv()
    install_dependencies()
    print("Setup complete! You can now run the app.")

if __name__ == "__main__":
    main()
