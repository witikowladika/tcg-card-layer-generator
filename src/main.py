"""
TCG Card Layer Generator - Main Entry Point

Generates professional print layers for trading cards from a single base artwork.
"""

import os
import sys
from PIL import Image, ImageOps

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    CARD_WIDTH_MM,
    CARD_HEIGHT_MM,
    DPI,
    WHITE_THRESHOLD,
    FOIL_THRESHOLD,
    SPOT_UV_EDGE_SIZE,
    INPUT_IMAGE,
    OUTPUT_LAYER_DIR,
    OUTPUT_PREVIEW_DIR,
)
from colors import POKEMON_COLORS, get_color
from layers import (
    prepare_canvas,
    generate_main_layer,
    generate_mask,
    generate_spot_uv,
)


def create_output_directories():
    """Ensure all output directories exist."""
    os.makedirs(OUTPUT_LAYER_DIR, exist_ok=True)
    os.makedirs(OUTPUT_PREVIEW_DIR, exist_ok=True)


def generate_preview(main_layer, white_layer, foil_layer, spot_layer, card_width, card_height):
    """
    Generate a 2x2 grid preview showing all layers side by side.
    
    Args:
        main_layer: Main color layer (RGB)
        white_layer: White ink mask (L)
        foil_layer: Foil mask (L)
        spot_layer: Spot UV mask (L)
        card_width: Card width in pixels
        card_height: Card height in pixels
        
    Returns:
        Preview PIL Image (RGB)
    """
    preview = Image.new("RGB", (card_width * 2, card_height * 2))
    
    # Top-left: Main color layer
    preview.paste(main_layer, (0, 0))
    
    # Top-right: White layer (colorized)
    white_preview = ImageOps.colorize(white_layer, black="black", white="white")
    preview.paste(white_preview, (card_width, 0))
    
    # Bottom-left: Foil layer (colorized in gold)
    foil_preview = ImageOps.colorize(foil_layer, black="black", white="gold")
    preview.paste(foil_preview, (0, card_height))
    
    # Bottom-right: Spot UV layer (colorized in cyan)
    spot_preview = ImageOps.colorize(spot_layer, black="black", white="cyan")
    preview.paste(spot_preview, (card_width, card_height))
    
    return preview


def main(theme: str = "grass"):
    """
    Main processing function.
    
    Args:
        theme: Color theme name (default: "grass")
              Available: grass, fire, water, lightning, psychic, fighting,
                        darkness, metal, dragon, fairy, colorless
    """
    print(f"🎨 TCG Card Layer Generator")
    print(f"📋 Theme: {theme}")
    print()
    
    # Validate theme
    try:
        color = get_color(theme)
    except KeyError as e:
        print(f"❌ Error: {e}")
        return
    
    # Create output directories
    create_output_directories()
    
    # Check if input file exists
    if not os.path.exists(INPUT_IMAGE):
        print(f"❌ Error: Input image not found at '{INPUT_IMAGE}'")
        print(f"   Please place your base artwork at: {INPUT_IMAGE}")
        return
    
    print(f"📥 Loading: {INPUT_IMAGE}")
    
    # Load and prepare image
    try:
        img = Image.open(INPUT_IMAGE).convert("RGB")
        print(f"   Original size: {img.size[0]}x{img.size[1]} px")
        
        img = prepare_canvas(img, CARD_WIDTH_MM, CARD_HEIGHT_MM, DPI)
        print(f"   Prepared size: {img.size[0]}x{img.size[1]} px ({CARD_WIDTH_MM}x{CARD_HEIGHT_MM} mm @ {DPI} DPI)")
        
    except Exception as e:
        print(f"❌ Error loading image: {e}")
        return
    
    # Convert to grayscale for processing
    gray = ImageOps.grayscale(img)
    
    print()
    print("🔧 Generating layers...")
    
    # Generate all layers
    main_layer = generate_main_layer(gray, color)
    white_layer = generate_mask(gray, WHITE_THRESHOLD)
    foil_layer = generate_mask(gray, FOIL_THRESHOLD)
    spot_layer = generate_spot_uv(gray, SPOT_UV_EDGE_SIZE)
    
    # Save individual layers
    main_path = f"{OUTPUT_LAYER_DIR}/main_color.png"
    white_path = f"{OUTPUT_LAYER_DIR}/white_layer.png"
    foil_path = f"{OUTPUT_LAYER_DIR}/foil_layer.png"
    spot_path = f"{OUTPUT_LAYER_DIR}/spot_uv_layer.png"
    
    main_layer.save(main_path)
    white_layer.save(white_path)
    foil_layer.save(foil_path)
    spot_layer.save(spot_path)
    
    print(f"   ✓ Main color layer: {main_path}")
    print(f"   ✓ White layer: {white_path}")
    print(f"   ✓ Foil layer: {foil_path}")
    print(f"   ✓ Spot UV layer: {spot_path}")
    
    # Generate and save preview
    preview = generate_preview(
        main_layer, white_layer, foil_layer, spot_layer,
        img.width, img.height
    )
    
    preview_path = f"{OUTPUT_PREVIEW_DIR}/layer_preview.png"
    preview.save(preview_path)
    print(f"   ✓ Preview: {preview_path}")
    
    print()
    print("✔ All layers successfully generated!")
    print(f"   Output directory: {os.path.dirname(OUTPUT_LAYER_DIR)}/")


if __name__ == "__main__":
    # Allow theme selection via command line argument
    theme = sys.argv[1] if len(sys.argv) > 1 else "grass"
    main(theme)

