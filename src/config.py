"""
Configuration settings for TCG Card Layer Generator.

All print and processing parameters are centralized here for easy modification.
"""

# ==============================
# CARD DIMENSIONS
# ==============================

# Standard Trading Card dimensions in millimeters
CARD_WIDTH_MM = 63
CARD_HEIGHT_MM = 88

# Print resolution in dots per inch (minimum 360 DPI for high-quality printing)
DPI = 360

# ==============================
# LAYER GENERATION THRESHOLDS
# ==============================

# Grayscale threshold for white ink layer (0-255)
# Higher values = more white ink coverage
WHITE_THRESHOLD = 140

# Grayscale threshold for foil layer (0-255)
# Higher values = more foil coverage
FOIL_THRESHOLD = 200

# Edge detection filter size for Spot UV layer
# Must be odd number >= 3 (e.g., 3, 5, 7, 9)
SPOT_UV_EDGE_SIZE = 3

# ==============================
# FILE PATHS
# ==============================

# Input image paths (relative to project root)
INPUT_IMAGE = "input/card_base.png"  # For backside generator
INPUT_FRONT_IMAGE = "input/card_front.png"  # For front generator

# Output directories (relative to project root)
OUTPUT_LAYER_DIR = "output/layers"
OUTPUT_PREVIEW_DIR = "output/preview"

