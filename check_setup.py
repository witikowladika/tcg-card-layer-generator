"""
Setup Check Script - Prüft ob alle Dependencies installiert sind
"""
import sys

print("=" * 60)
print("TCG Card Layer Generator - Setup Check")
print("=" * 60)
print(f"\nPython Version: {sys.version}")
print(f"Python Executable: {sys.executable}")
print(f"Python Path: {sys.executable}")

# Check PIL/Pillow
print("\n" + "-" * 60)
print("Checking PIL/Pillow...")
try:
    from PIL import Image, ImageOps, ImageFilter
    print("✓ PIL/Pillow is installed")
    print(f"  Version: {Image.__version__}")
    print(f"  Location: {Image.__file__}")
except ImportError as e:
    print("✗ PIL/Pillow is NOT installed!")
    print(f"  Error: {e}")
    print("\n  To install, run:")
    print(f"    {sys.executable} -m pip install Pillow")
    sys.exit(1)

# Check NumPy
print("\n" + "-" * 60)
print("Checking NumPy...")
try:
    import numpy as np
    print("✓ NumPy is installed")
    print(f"  Version: {np.__version__}")
    print(f"  Location: {np.__file__}")
except ImportError as e:
    print("✗ NumPy is NOT installed!")
    print(f"  Error: {e}")
    print("\n  To install, run:")
    print(f"    {sys.executable} -m pip install numpy")
    sys.exit(1)

# Check project files
print("\n" + "-" * 60)
print("Checking project files...")
import os

files_to_check = [
    "src/config.py",
    "src/colors.py",
    "src/layers.py",
    "src/main.py",
]

all_ok = True
for file in files_to_check:
    if os.path.exists(file):
        print(f"✓ {file}")
    else:
        print(f"✗ {file} - NOT FOUND")
        all_ok = False

if not all_ok:
    print("\n⚠ Some project files are missing!")
    sys.exit(1)

# Try importing project modules
print("\n" + "-" * 60)
print("Testing project imports...")
try:
    sys.path.insert(0, "src")
    from config import INPUT_IMAGE
    print("✓ Config imported successfully")
    from colors import POKEMON_COLORS
    print("✓ Colors imported successfully")
    from layers import prepare_canvas
    print("✓ Layers imported successfully")
except ImportError as e:
    print(f"✗ Project import failed: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✔ All checks passed! Setup is correct.")
print("=" * 60)
print("\nYou can now run the generator with:")
print("  python src\\main.py")
print("\nOr with a specific theme:")
print("  python src\\main.py fire")

