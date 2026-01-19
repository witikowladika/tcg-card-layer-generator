"""
TCG Card Front Generator - Automatic detection and layer generation

Automatically detects card variant (shiny/holo/normal) and type (grass, fire, etc.)
from card_front.png and generates appropriate layers.
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
    OUTPUT_LAYER_DIR,
    OUTPUT_PREVIEW_DIR,
    INPUT_FRONT_IMAGE,
    INPUT_IMAGE,
)
from colors import POKEMON_COLORS, get_color, get_shiny_color, RAINBOW_COLORS
from layers import (
    prepare_canvas,
    generate_main_layer,
    generate_mask,
    generate_spot_uv,
    generate_rainbow_layer,
    generate_holo_layer,
)
from detection import detect_variant, detect_type


def generate_front_layers(input_image_path: str = None, auto_detect: bool = True, 
                          theme: str = None, variant: str = None, output_prefix: str = None):
    """
    Generate layers for a single card front image with automatic detection.
    
    Args:
        input_image_path: Path to the input front image (default: "input/card_front.png")
        auto_detect: If True, automatically detect variant and type
        theme: Override type detection with manual theme (e.g., "grass", "fire")
        variant: Override variant detection with manual variant ("shiny", "holo", "normal")
        output_prefix: Optional prefix for output files (default: auto-generated from detections)
    
    Returns:
        True if successful, False otherwise
    """
    print(f"🎨 TCG Card Front Generator")
    print(f"🔍 Automatic Detection Mode")
    print()
    
    # Determine input image path
    if input_image_path is None:
        # Use configured front image path
        if os.path.exists(INPUT_FRONT_IMAGE):
            input_image_path = INPUT_FRONT_IMAGE
        elif os.path.exists("input/card_front.png"):
            input_image_path = "input/card_front.png"
        else:
            print(f"❌ Error: No input image found")
            print(f"   Please place your card front at: {INPUT_FRONT_IMAGE}")
            return False
    
    # Check if input file exists
    if not os.path.exists(input_image_path):
        print(f"❌ Error: Input image not found at '{input_image_path}'")
        return False
    
    print(f"📥 Loading: {input_image_path}")
    
    # Load and prepare image (keep original for detection, then prepare canvas)
    try:
        img_original = Image.open(input_image_path).convert("RGB")
        print(f"   Original size: {img_original.size[0]}x{img_original.size[1]} px")
        
        # Detect variant and type BEFORE preparing canvas
        detected_variant = None
        detected_type = None
        
        if auto_detect:
            print()
            print("🔍 Analyzing card...")
            detected_variant = detect_variant(img_original)
            detected_type = detect_type(img_original)
            print(f"   ✓ Detected Variant: {detected_variant.capitalize()}")
            print(f"   ✓ Detected Type: {detected_type.capitalize()}")
        else:
            if variant is None:
                detected_variant = "normal"
            else:
                detected_variant = variant.lower()
            
            if theme is None:
                detected_type = detect_type(img_original)
                print(f"   ✓ Detected Type: {detected_type.capitalize()}")
            else:
                detected_type = theme.lower()
        
        # Now prepare canvas for layer generation
        img = prepare_canvas(img_original, CARD_WIDTH_MM, CARD_HEIGHT_MM, DPI)
        print(f"   Prepared size: {img.size[0]}x{img.size[1]} px ({CARD_WIDTH_MM}x{CARD_HEIGHT_MM} mm @ {DPI} DPI)")
        
    except Exception as e:
        print(f"❌ Error loading image: {e}")
        return False
    
    # Override with manual settings if provided
    if variant:
        detected_variant = variant.lower()
        print(f"   ⚙️  Using manual variant: {detected_variant}")
    
    if theme:
        detected_type = theme.lower()
        print(f"   ⚙️  Using manual theme: {detected_type}")
    
    # Validate detected type
    if detected_type not in POKEMON_COLORS:
        print(f"❌ Error: Invalid type '{detected_type}'")
        print(f"   Available types: {', '.join(POKEMON_COLORS.keys())}")
        return False
    
    # Get base color for the type
    base_color = get_color(detected_type)
    
    print()
    print("🔧 Generating layers...")
    print(f"   Type: {detected_type.capitalize()}, Variant: {detected_variant.capitalize()}")
    
    # Convert to grayscale for processing
    gray = ImageOps.grayscale(img)
    
    # Generate main color layer based on variant
    if detected_variant == "rainbow":
        main_layer = generate_rainbow_layer(gray, RAINBOW_COLORS)
        variant_suffix = "rainbow"
    elif detected_variant == "shiny":
        shiny_color = get_shiny_color(base_color)
        main_layer = generate_main_layer(gray, shiny_color)
        variant_suffix = "shiny"
    elif detected_variant == "holo":
        main_layer = generate_holo_layer(gray, base_color)
        variant_suffix = "holo"
    else:  # normal
        main_layer = generate_main_layer(gray, base_color)
        variant_suffix = "normal"
    
    # Generate other layers (same for all variants)
    white_layer = generate_mask(gray, WHITE_THRESHOLD)
    foil_layer = generate_mask(gray, FOIL_THRESHOLD)
    spot_layer = generate_spot_uv(gray, SPOT_UV_EDGE_SIZE)
    
    # Determine output prefix
    if output_prefix is None:
        if variant_suffix == "normal":
            output_prefix = detected_type
        else:
            output_prefix = f"{detected_type}_{variant_suffix}"
    
    # Create output directory
    output_dir = os.path.join(OUTPUT_LAYER_DIR, "fronts", output_prefix)
    preview_dir = os.path.join(OUTPUT_PREVIEW_DIR, "fronts", output_prefix)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(preview_dir, exist_ok=True)
    
    # Save individual layers
    main_path = os.path.join(output_dir, "main_color.png")
    white_path = os.path.join(output_dir, "white_layer.png")
    foil_path = os.path.join(output_dir, "foil_layer.png")
    spot_path = os.path.join(output_dir, "spot_uv_layer.png")
    
    main_layer.save(main_path)
    white_layer.save(white_path)
    foil_layer.save(foil_path)
    spot_layer.save(spot_path)
    
    print(f"   ✓ Main color layer: {main_path}")
    print(f"   ✓ White layer: {white_path}")
    print(f"   ✓ Foil layer: {foil_path}")
    print(f"   ✓ Spot UV layer: {spot_path}")
    
    # Generate simple preview (single image showing main layer)
    preview_path = os.path.join(preview_dir, "preview.png")
    main_layer.save(preview_path)
    print(f"   ✓ Preview: {preview_path}")
    
    print()
    print("✔ Front layers successfully generated!")
    print(f"   Output directory: {output_dir}/")
    print(f"   Type: {detected_type.capitalize()}, Variant: {detected_variant.capitalize()}")
    
    # Generate matching backside layers
    print()
    print("🔄 Generating matching backside layers...")
    backside_success = generate_matching_backside(detected_type, detected_variant)
    
    if backside_success:
        print("✔ Backside layers successfully generated!")
    else:
        print("⚠️  Backside generation failed (front layers are still saved)")
    
    return True


def generate_matching_backside(theme: str, variant: str) -> bool:
    """
    Generate backside layers matching the detected front card type and variant.
    
    Args:
        theme: Type name (e.g., "grass", "fire")
        variant: Variant name ("normal", "shiny", "holo", "rainbow")
        
    Returns:
        True if successful, False otherwise
    """
    # Check if backside base image exists
    if not os.path.exists(INPUT_IMAGE):
        print(f"   ⚠️  Backside base image not found at '{INPUT_IMAGE}'")
        print(f"      Skipping backside generation")
        return False
    
    try:
        # Load backside base image
        backside_img = Image.open(INPUT_IMAGE).convert("RGB")
        backside_img = prepare_canvas(backside_img, CARD_WIDTH_MM, CARD_HEIGHT_MM, DPI)
        backside_gray = ImageOps.grayscale(backside_img)
        
        # Determine theme directory name
        if variant == "normal":
            theme_dir = theme
            theme_name = theme
        else:
            theme_dir = f"{theme}_{variant}"
            theme_name = f"{theme}_{variant}"
        
        # Create output directories
        backside_layer_dir = os.path.join(OUTPUT_LAYER_DIR, theme_dir)
        backside_preview_dir = os.path.join(OUTPUT_PREVIEW_DIR, theme_dir)
        os.makedirs(backside_layer_dir, exist_ok=True)
        os.makedirs(backside_preview_dir, exist_ok=True)
        
        # Get base color for the type
        base_color = get_color(theme)
        
        # Generate main color layer based on variant
        if variant == "rainbow":
            main_layer = generate_rainbow_layer(backside_gray, RAINBOW_COLORS)
        elif variant == "shiny":
            shiny_color = get_shiny_color(base_color)
            main_layer = generate_main_layer(backside_gray, shiny_color)
        elif variant == "holo":
            main_layer = generate_holo_layer(backside_gray, base_color)
        else:  # normal
            main_layer = generate_main_layer(backside_gray, base_color)
        
        # Generate other layers
        white_layer = generate_mask(backside_gray, WHITE_THRESHOLD)
        foil_layer = generate_mask(backside_gray, FOIL_THRESHOLD)
        spot_layer = generate_spot_uv(backside_gray, SPOT_UV_EDGE_SIZE)
        
        # Save backside layers
        main_path = os.path.join(backside_layer_dir, "main_color.png")
        white_path = os.path.join(backside_layer_dir, "white_layer.png")
        foil_path = os.path.join(backside_layer_dir, "foil_layer.png")
        spot_path = os.path.join(backside_layer_dir, "spot_uv_layer.png")
        
        main_layer.save(main_path)
        white_layer.save(white_path)
        foil_layer.save(foil_path)
        spot_layer.save(spot_path)
        
        # Generate preview (2x2 grid)
        card_width = main_layer.width
        card_height = main_layer.height
        preview = Image.new("RGB", (card_width * 2, card_height * 2))
        
        preview.paste(main_layer, (0, 0))
        white_preview = ImageOps.colorize(white_layer, black=(0, 0, 0), white=(255, 255, 255))
        preview.paste(white_preview, (card_width, 0))
        foil_preview = ImageOps.colorize(foil_layer, black=(0, 0, 0), white=(255, 215, 0))
        preview.paste(foil_preview, (0, card_height))
        spot_preview = ImageOps.colorize(spot_layer, black=(0, 0, 0), white=(0, 255, 255))
        preview.paste(spot_preview, (card_width, card_height))
        
        preview_path = os.path.join(backside_preview_dir, "layer_preview.png")
        preview.save(preview_path)
        
        print(f"   ✓ Backside layers saved to {backside_layer_dir}/")
        return True
        
    except Exception as e:
        print(f"   ❌ Error generating backside: {e}")
        return False


if __name__ == "__main__":
    # Parse command line arguments
    # Usage: 
    #   python src/front_generator.py                          # Auto-detect from input/card_front.png
    #   python src/front_generator.py <image_path>            # Auto-detect from custom image
    #   python src/front_generator.py <image_path> <theme>    # Override type
    #   python src/front_generator.py <image_path> <theme> <variant>  # Override both
    
    input_image = None
    theme = None
    variant = None
    output_prefix = None
    
    if len(sys.argv) == 1:
        # No arguments: use default card_front.png with auto-detection
        print("🔍 Auto-detecting from input/card_front.png...")
        success = generate_front_layers(auto_detect=True)
    elif len(sys.argv) == 2:
        # One argument: custom image path with auto-detection
        input_image = sys.argv[1]
        success = generate_front_layers(input_image_path=input_image, auto_detect=True)
    elif len(sys.argv) == 3:
        # Two arguments: image path + theme (override type detection)
        input_image = sys.argv[1]
        theme = sys.argv[2].lower()
        
        # Check if it's actually a variant name
        if theme in ["normal", "shiny", "holo", "rainbow"]:
            variant = theme
            theme = None
            success = generate_front_layers(input_image_path=input_image, auto_detect=True, variant=variant)
        else:
            success = generate_front_layers(input_image_path=input_image, auto_detect=True, theme=theme)
    elif len(sys.argv) == 4:
        # Three arguments: image path + theme + variant (override both)
        input_image = sys.argv[1]
        theme = sys.argv[2].lower()
        variant = sys.argv[3].lower()
        success = generate_front_layers(
            input_image_path=input_image, 
            auto_detect=False,
            theme=theme, 
            variant=variant
        )
    else:
        print("Usage:")
        print("  python src/front_generator.py                                    # Auto-detect from input/card_front.png")
        print("  python src/front_generator.py <image_path>                      # Auto-detect from custom image")
        print("  python src/front_generator.py <image_path> <theme>              # Override type detection")
        print("  python src/front_generator.py <image_path> <theme> <variant>    # Override type and variant")
        print()
        print("Examples:")
        print("  python src/front_generator.py                                    # Auto-detect everything")
        print("  python src/front_generator.py input/card_front.png               # Auto-detect from custom image")
        print("  python src/front_generator.py input/card_front.png fire          # Force fire type")
        print("  python src/front_generator.py input/card_front.png fire shiny    # Force fire + shiny")
        print()
        print("Available themes:", ", ".join(POKEMON_COLORS.keys()))
        print("Available variants: normal, shiny, holo, rainbow")
        sys.exit(1)
    
    sys.exit(0 if success else 1)

