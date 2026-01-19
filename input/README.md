# Input Directory

## Card Backsides

Place your base artwork here as `card_base.png` for backside generation.

## Card Fronts

Place your card front image here as `card_front.png` for automatic front layer generation.

**Automatic Detection:**
The front generator will automatically detect:
- **Variant**: shiny, holo, rainbow, or normal (from border analysis)
- **Type**: grass, fire, water, etc. (from dominant color analysis)

## Requirements

- **File names**: 
  - `card_base.png` - For backside generation
  - `card_front.png` - For front generation (automatic detection)
- **Format**: PNG, JPEG, or any PIL-supported format
- **Aspect ratio**: Any (will be center-cropped to card ratio)
- **Resolution**: Higher is better (recommended: 2000+ pixels wide)
- **Color mode**: Any (will be converted to RGB)

The tool will automatically:
- Center-crop to match the card aspect ratio (63:88)
- Resize to exact print dimensions (63×88 mm @ 300 DPI)
- Detect variant and type from card front images

