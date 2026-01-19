"""
Install Dependencies Script - Installiert alle benötigten Pakete
"""
import subprocess
import sys

def install_package(package):
    """Installiert ein Python-Paket"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install {package}: {e}")
        return False

def main():
    print("=" * 60)
    print("TCG Card Layer Generator - Dependency Installer")
    print("=" * 60)
    print(f"\nUsing Python: {sys.executable}")
    print(f"Python Version: {sys.version}\n")
    
    packages = [
        "Pillow>=9.0.0",
        "numpy>=1.20.0"
    ]
    
    print("Installing dependencies...\n")
    
    success = True
    for package in packages:
        print(f"Installing {package}...")
        if not install_package(package):
            success = False
        print()
    
    if success:
        print("=" * 60)
        print("✔ All dependencies installed successfully!")
        print("=" * 60)
        print("\nRun 'python check_setup.py' to verify installation.")
    else:
        print("=" * 60)
        print("✗ Some dependencies failed to install.")
        print("=" * 60)
        print("\nTry installing manually:")
        print(f"  {sys.executable} -m pip install Pillow numpy")

if __name__ == "__main__":
    main()

