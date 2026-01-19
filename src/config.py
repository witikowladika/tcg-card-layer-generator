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

# Print resolution in dots per inch
DPI = 300

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
SPOT_UV_EDGE_SIZE = 2

# ==============================
# FILE PATHS
# ==============================

# Input image path (relative to project root)
INPUT_IMAGE = "input/card_base.png"

# Output directories (relative to project root)
OUTPUT_LAYER_DIR = "output/layers"
OUTPUT_PREVIEW_DIR = "output/preview"

