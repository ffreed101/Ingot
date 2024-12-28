import os
import subprocess
import sys

def create_virtualenv():
    """Create a virtual environment."""
    print("Creating virtual environment...")
    # Use Python's built-in venv module to create the environment
    subprocess.run([sys.executable, "-m", "venv", "venv"])
    print("Virtual environment created in the 'venv' folder.")

def install_dependencies():
    """Install dependencies using pip."""
    print("Installing dependencies...")
    if os.name == "nt":  # For Windows
        activate_script = ".\\venv\\Scripts\\activate.bat"
    else:  # For macOS/Linux
        activate_script = "source ./venv/bin/activate"

    # Use a shell command to activate the virtual environment and install requirements
    command = f"{activate_script} && pip install -r requirements.txt"
    os.system(command)
    print("Dependencies installed!")

def main():
    """Main function to orchestrate the setup."""
    print("Starting setup process...")
    create_virtualenv()
    install_dependencies()
    print("Setup complete! You can now run the app.")