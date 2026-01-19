"""
TCG Card Backside Generator - Generates all variants (normal, shiny, holo, rainbow)

Generates professional print layers for trading card backsides with full variant support.
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
from colors import POKEMON_COLORS, get_color, get_shiny_color, RAINBOW_COLORS
from layers import (
    prepare_canvas,
    generate_main_layer,
    generate_mask,
    generate_spot_uv,
    generate_rainbow_layer,
    generate_holo_layer,
)


def create_output_directories(theme: str = None):
    """Ensure all output directories exist.
    
    Args:
        theme: Optional theme name for theme-specific subdirectories
    """
    if theme:
        theme_layer_dir = os.path.join(OUTPUT_LAYER_DIR, theme)
        theme_preview_dir = os.path.join(OUTPUT_PREVIEW_DIR, theme)
        os.makedirs(theme_layer_dir, exist_ok=True)
        os.makedirs(theme_preview_dir, exist_ok=True)
    else:
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
    # Convert grayscale to RGB by mapping black->black, white->white
    white_preview = ImageOps.colorize(white_layer, black=(0, 0, 0), white=(255, 255, 255))
    preview.paste(white_preview, (card_width, 0))
    
    # Bottom-left: Foil layer (colorized in gold)
    # Map black->black, white->gold (RGB: 255, 215, 0)
    foil_preview = ImageOps.colorize(foil_layer, black=(0, 0, 0), white=(255, 215, 0))
    preview.paste(foil_preview, (0, card_height))
    
    # Bottom-right: Spot UV layer (colorized in cyan)
    # Map black->black, white->cyan (RGB: 0, 255, 255)
    spot_preview = ImageOps.colorize(spot_layer, black=(0, 0, 0), white=(0, 255, 255))
    preview.paste(spot_preview, (card_width, card_height))
    
    return preview


def generate_theme_layers(theme: str, gray_img: Image.Image, img_size: tuple, variant: str = "normal") -> bool:
    """
    Generate layers for a specific theme and variant.
    
    Args:
        theme: Color theme name
        gray_img: Pre-processed grayscale image
        img_size: Tuple of (width, height) in pixels
        variant: Variant type - "normal", "shiny", "holo", or "rainbow"
        
    Returns:
        True if successful, False otherwise
    """
    # Handle rainbow variant (no base theme needed)
    if variant == "rainbow":
        theme_name = "rainbow"
        theme_dir = "rainbow"
    else:
        # Validate theme for other variants
        try:
            base_color = get_color(theme)
        except KeyError as e:
            print(f"   ❌ Error: {e}")
            return False
        
        theme_name = f"{theme}_{variant}" if variant != "normal" else theme
        theme_dir = f"{theme}_{variant}" if variant != "normal" else theme
    
    # Create theme-specific output directories
    create_output_directories(theme_dir)
    
    theme_layer_dir = os.path.join(OUTPUT_LAYER_DIR, theme_dir)
    theme_preview_dir = os.path.join(OUTPUT_PREVIEW_DIR, theme_dir)
    
    # Generate main color layer based on variant
    if variant == "rainbow":
        main_layer = generate_rainbow_layer(gray_img, RAINBOW_COLORS)
    elif variant == "shiny":
        shiny_color = get_shiny_color(base_color)
        main_layer = generate_main_layer(gray_img, shiny_color)
    elif variant == "holo":
        main_layer = generate_holo_layer(gray_img, base_color)
    else:  # normal
        main_layer = generate_main_layer(gray_img, base_color)
    
    # Generate other layers (same for all variants)
    white_layer = generate_mask(gray_img, WHITE_THRESHOLD)
    foil_layer = generate_mask(gray_img, FOIL_THRESHOLD)
    spot_layer = generate_spot_uv(gray_img, SPOT_UV_EDGE_SIZE)
    
    # Save individual layers
    main_path = os.path.join(theme_layer_dir, "main_color.png")
    white_path = os.path.join(theme_layer_dir, "white_layer.png")
    foil_path = os.path.join(theme_layer_dir, "foil_layer.png")
    spot_path = os.path.join(theme_layer_dir, "spot_uv_layer.png")
    
    main_layer.save(main_path)
    white_layer.save(white_path)
    foil_layer.save(foil_path)
    spot_layer.save(spot_path)
    
    # Generate and save preview
    # Get dimensions from generated layer (more reliable than img_size tuple)
    card_width = main_layer.width
    card_height = main_layer.height
    preview = generate_preview(
        main_layer, white_layer, foil_layer, spot_layer,
        card_width, card_height
    )
    
    preview_path = os.path.join(theme_preview_dir, "layer_preview.png")
    preview.save(preview_path)
    
    print(f"   ✓ {theme_name.capitalize()}: layers saved to {theme_layer_dir}/")
    return True


def main(theme: str = "grass", batch_mode: bool = False, input_image_path: str = None, variant: str = "all"):
    """
    Main processing function for backside generation.
    
    Args:
        theme: Color theme name (default: "grass") or "all" for batch mode
        batch_mode: If True, generate all themes (overrides theme parameter)
        input_image_path: Optional custom input image path
        variant: Variant type - "normal", "shiny", "holo", "rainbow", or "all" (default: "all")
    """
    print(f"🎨 TCG Card Backside Generator")
    
    # Use custom input image if provided, otherwise use default
    image_to_process = input_image_path if input_image_path else INPUT_IMAGE
    
    # If custom image is provided, only process single theme (not batch)
    if input_image_path:
        if theme.lower() == "all":
            print("⚠️  Custom input image provided - batch mode disabled")
            print("   Processing only the specified theme (use specific theme name)")
            theme = "grass"  # Default to grass if "all" was specified
        themes_to_process = [theme]
        print(f"📋 Theme: {theme}")
        print(f"📷 Custom Input: {input_image_path}")
    elif batch_mode or theme.lower() == "all":
        themes_to_process = list(POKEMON_COLORS.keys())
        print(f"📋 Batch Mode: Generating all {len(themes_to_process)} themes")
    else:
        themes_to_process = [theme]
        print(f"📋 Theme: {theme}")
    
    print()
    
    # Check if input file exists
    if not os.path.exists(image_to_process):
        print(f"❌ Error: Input image not found at '{image_to_process}'")
        if input_image_path:
            print(f"   Please check the file path.")
        else:
            print(f"   Please place your base artwork at: {INPUT_IMAGE}")
        return
    
    print(f"📥 Loading: {image_to_process}")
    
    # Load and prepare image (only once for batch mode)
    try:
        img = Image.open(image_to_process).convert("RGB")
        print(f"   Original size: {img.size[0]}x{img.size[1]} px")
        
        img = prepare_canvas(img, CARD_WIDTH_MM, CARD_HEIGHT_MM, DPI)
        print(f"   Prepared size: {img.size[0]}x{img.size[1]} px ({CARD_WIDTH_MM}x{CARD_HEIGHT_MM} mm @ {DPI} DPI)")
        
    except Exception as e:
        print(f"❌ Error loading image: {e}")
        return
    
    # Determine variants to process
    if variant.lower() == "all":
        variants_to_process = ["normal", "shiny", "holo"]
        print(f"✨ Variants: Normal, Shiny, Holo (and Rainbow)")
    elif variant.lower() == "rainbow":
        variants_to_process = []  # Rainbow is handled separately
        print(f"✨ Variant: Rainbow")
    else:
        variants_to_process = [variant.lower()]
        print(f"✨ Variant: {variant.capitalize()}")
    
    print()
    
    # Convert to grayscale for processing (only once for batch mode)
    gray = ImageOps.grayscale(img)
    img_size = (img.width, img.height)
    
    print()
    print("🔧 Generating layers...")
    print()
    
    # Process each theme and variant combination
    successful = 0
    failed = 0
    rainbow_generated = False
    
    # Handle rainbow-only mode
    if variant.lower() == "rainbow":
        if theme.lower() not in POKEMON_COLORS or theme.lower() == "rainbow":
            if generate_theme_layers("", gray, img_size, "rainbow"):
                successful += 1
            else:
                failed += 1
            rainbow_generated = True
    else:
        for current_theme in themes_to_process:
            if len(themes_to_process) > 1:
                print(f"  Processing {current_theme}...")
            
            # Generate all variants for this theme
            for current_variant in variants_to_process:
                if generate_theme_layers(current_theme, gray, img_size, current_variant):
                    successful += 1
                else:
                    failed += 1
            
            # Add rainbow variant if "all" variants requested (once per batch, not per theme)
            if variant.lower() == "all" and not rainbow_generated:
                if generate_theme_layers("", gray, img_size, "rainbow"):
                    successful += 1
                    rainbow_generated = True
                else:
                    failed += 1
    
    print()
    print("=" * 60)
    print(f"✔ Generation complete!")
    total_expected = len(themes_to_process) * len(variants_to_process)
    if variant.lower() == "all" and not rainbow_generated:
        total_expected += 1  # Add one rainbow variant
    if rainbow_generated and variant.lower() == "rainbow":
        total_expected = 1
    print(f"   Successful: {successful}/{total_expected}")
    if failed > 0:
        print(f"   Failed: {failed}/{total_expected}")
    print(f"   Output directory: {OUTPUT_LAYER_DIR}/")
    print("=" * 60)


if __name__ == "__main__":
    # Parse command line arguments
    variant = "all"  # Default to all variants
    image_path = None
    
    if len(sys.argv) == 1:
        # No arguments: generate all themes, all variants with default image
        main(theme="all", batch_mode=True, variant="all")
    elif len(sys.argv) == 2:
        # One argument: theme name
        theme_arg = sys.argv[1].lower()
        if theme_arg == "all":
            main(theme="all", batch_mode=True, variant="all")
        elif theme_arg in ["normal", "shiny", "holo", "rainbow"]:
            # Variant without theme - assume "all" themes
            main(theme="all", batch_mode=True, variant=theme_arg)
        else:
            main(theme=theme_arg, variant="all")
    elif len(sys.argv) == 3:
        # Two arguments: could be theme + variant OR theme + image
        arg1 = sys.argv[1].lower()
        arg2 = sys.argv[2]  # Keep original case for file paths
        
        # Check if arg2 is a variant name (case-insensitive)
        arg2_lower = arg2.lower()
        if arg2_lower in ["normal", "shiny", "holo", "rainbow"]:
            # Theme + variant
            if arg1 == "all":
                main(theme="all", batch_mode=True, variant=arg2_lower)
            else:
                main(theme=arg1, variant=arg2_lower)
        elif os.path.exists(arg2) or arg2.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Theme + image path (use original case)
            if arg1 == "all":
                print("⚠️  'all' theme not supported with custom image")
                print("   Please specify a specific theme name")
                sys.exit(1)
            if arg1 not in POKEMON_COLORS:
                print(f"❌ Error: Unknown theme '{arg1}'")
                print(f"   Available themes: {', '.join(POKEMON_COLORS.keys())}")
                sys.exit(1)
            main(theme=arg1, input_image_path=arg2, variant="all")
        else:
            print(f"❌ Error: Invalid argument '{arg2}'")
            print("   Expected: variant name (normal/shiny/holo/rainbow) or image path")
            sys.exit(1)
    elif len(sys.argv) == 4:
        # Three arguments: theme + variant + image
        theme_arg = sys.argv[1].lower()
        variant_arg = sys.argv[2].lower()
        image_path = sys.argv[3]
        
        if theme_arg == "all":
            print("⚠️  'all' theme not supported with custom image")
            print("   Please specify a specific theme name")
            sys.exit(1)
        
        if theme_arg not in POKEMON_COLORS:
            print(f"❌ Error: Unknown theme '{theme_arg}'")
            print(f"   Available themes: {', '.join(POKEMON_COLORS.keys())}")
            sys.exit(1)
        
        if variant_arg not in ["normal", "shiny", "holo", "rainbow", "all"]:
            print(f"❌ Error: Unknown variant '{variant_arg}'")
            print("   Available variants: normal, shiny, holo, rainbow, all")
            sys.exit(1)
        
        main(theme=theme_arg, input_image_path=image_path, variant=variant_arg)
    else:
        print("Usage:")
        print("  python src/backside_generator.py                                    # All themes, all variants")
        print("  python src/backside_generator.py <theme>                            # Theme, all variants")
        print("  python src/backside_generator.py <theme> <variant>                  # Theme, specific variant")
        print("  python src/backside_generator.py <theme> <image_path>               # Theme, all variants, custom image")
        print("  python src/backside_generator.py <theme> <variant> <image_path>     # Theme, variant, custom image")
        print()
        print("Variants: normal, shiny, holo, rainbow, all (default: all)")
        sys.exit(1)

