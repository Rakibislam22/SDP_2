import subprocess
import sys

packages = [
    "customtkinter",
    "pillow",
    "google-generativeai",
    "CurrencyConverter"
]
def install_packages(packages):
    for need in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", need])
            print(f"Successfully installed {need}")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while installing {need}: {e}")

install_packages(packages)
