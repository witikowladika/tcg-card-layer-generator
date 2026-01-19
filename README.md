# TCG Card Layer Generator

A professional Python tool to generate print-ready layers for trading cards from a single high-quality base artwork. Designed for Pokémon-style cards with support for white ink, foil stamping, and spot UV effects.

## ✨ Features

- **Exact Aspect Ratio Preservation** - Maintains precise 63×88 mm card dimensions
- **Parametric Recoloring** - Apply any theme color while preserving luminance details
- **Batch Processing** - Generate all color themes at once with a single command
- **Card Variants** - Support for Normal, Shiny, Holo, and Rainbow variants
- **Print-Ready Layer Separation**:
  - Main color layer (CMYK-ready artwork)
  - White ink layer (underprinting mask)
  - Foil layer (hot foil stamping mask)
  - Spot UV / emboss layer (glossy finish mask)
- **Visual Preview Generation** - 2×2 grid showing all layers side-by-side
- **Pokémon-Style Color Themes** - Pre-configured color palettes for all 11 types

## 📋 Requirements

- Python 3.7+
- Pillow (PIL) >= 10.0.0
- NumPy >= 1.24.0

## 🚀 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd tcg-card-layer-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📖 Usage

### Basic Usage

1. Place your base artwork in `input/card_base.png`
   - Any aspect ratio is fine; the tool will center-crop to match card dimensions
   - Higher resolution is better (recommended: 2000+ pixels wide)

2. Run the generator:

## 📋 Two Generators Available

### 1. Backside Generator (`src/backside_generator.py`)
For generating card backsides with full variant support (normal, shiny, holo, rainbow).

**Available Themes:**
- `grass` - Green
- `fire` - Red
- `water` - Blue
- `lightning` - Yellow
- `psychic` - Purple
- `fighting` - Brown
- `darkness` - Dark gray
- `metal` - Silver gray
- `dragon` - Dark green
- `fairy` - Pink
- `colorless` - Light gray

**Variants:**
- **Normal**: Standard colors (default)
- **Shiny**: Brighter, more saturated versions of base colors
- **Holo**: Holographic/iridescent effect with color shifting
- **Rainbow**: Gradient through all type colors (red → yellow → green → blue → purple → pink)
- **All**: Generates normal, shiny, holo, and rainbow variants (default)

**Usage Examples:**
```bash
# Generate all themes with all variants (default)
python src/backside_generator.py
python src/backside_generator.py all

# Generate a specific theme (all variants)
python src/backside_generator.py grass
python src/backside_generator.py fire

# Generate specific variant only
python src/backside_generator.py fire shiny          # Shiny variant only
python src/backside_generator.py fire holo           # Holographic variant only
python src/backside_generator.py fire rainbow        # Rainbow variant (theme-agnostic)
python src/backside_generator.py rainbow             # Rainbow variant for all themes

# Generate from custom backside image
python src/backside_generator.py fire input/my_backside.png
```

### 2. Front Generator (`src/front_generator.py`)
**Automatic detection** of variant and type from card images. Analyzes the card to detect:
- **Variant**: shiny, holo, rainbow, or normal (detected from border patterns)
- **Type**: grass, fire, water, etc. (detected from dominant inner color)

**Automatic detection (recommended):**
```bash
# Auto-detect from input/card_front.png
python src/front_generator.py

# Auto-detect from custom image
python src/front_generator.py input/my_card_front.png
```

**Manual overrides:**
```bash
# Override type detection only
python src/front_generator.py input/my_card_front.png fire

# Override both type and variant
python src/front_generator.py input/my_card_front.png fire shiny
```

**How detection works:**
- **Variant detection**: Analyzes border edges (5-6% of image) for:
  - Rainbow: Extreme color variance with many unique colors
  - Holo: High color variance (rainbow shimmer effect)
  - Shiny: High saturation and brightness contrast (distinct patterns)
  - Normal: Consistent colors (default)
  
- **Type detection**: Analyzes inner region (excluding 10% border) for dominant color, matches to closest Pokémon type

**Note:** Place your card front at `input/card_front.png` for automatic processing.

### Quick Reference

**Backside Generator - Batch processing:**
- Generates all themes with all variants by default
- Supports custom input images
- Creates organized output structure with theme/variant folders

**Front Generator - Automatic detection:**
- Automatically detects variant (shiny/holo/rainbow/normal) from border patterns
- Automatically detects type (grass/fire/water/etc.) from dominant color
- Supports manual overrides if detection is incorrect
- Ideal for processing individual card fronts with correct variant matching

### Output Structure

After running, you'll find:

**Single theme mode:**
```
output/
├── layers/
│   ├── main_color.png      # CMYK-ready artwork
│   ├── white_layer.png     # White ink mask
│   ├── foil_layer.png      # Foil stamping mask
│   └── spot_uv_layer.png   # Spot UV / emboss mask
│
└── preview/
    └── layer_preview.png   # Visual control (2×2 grid)
```

**Batch mode (all themes, all variants):**
```
output/
├── layers/
│   ├── grass/
│   │   ├── main_color.png
│   │   ├── white_layer.png
│   │   ├── foil_layer.png
│   │   └── spot_uv_layer.png
│   ├── grass_shiny/
│   │   └── ... (shiny variant)
│   ├── grass_holo/
│   │   └── ... (holo variant)
│   ├── fire/
│   │   └── ...
│   ├── fire_shiny/
│   │   └── ...
│   ├── rainbow/
│   │   └── ... (rainbow gradient)
│   └── ... (all themes and variants)
│
└── preview/
    └── ... (preview for each variant)
```

## ⚙️ Configuration

Edit `src/config.py` to customize:

- **Card Dimensions**: `CARD_WIDTH_MM`, `CARD_HEIGHT_MM`
- **Print Resolution**: `DPI` (default: 300)
- **Layer Thresholds**: `WHITE_THRESHOLD`, `FOIL_THRESHOLD`
- **Edge Detection**: `SPOT_UV_EDGE_SIZE`

### Custom Colors

Add custom colors in `src/colors.py`:

```python
POKEMON_COLORS = {
    "custom_theme": (R, G, B),
    # ... existing themes
}
```

Then use it:
```bash
python src/backside_generator.py custom_theme
```

## 🖨️ Print Notes

- **Designed for**: 63 × 88 mm trading cards @ 300 DPI
- **Compatible with**: White ink workflows, hot foil stamping, spot UV printing
- **No AI Re-generation** - Original geometry and details are preserved exactly
- **CMYK Conversion**: The main color layer should be converted to CMYK by your print shop if needed

## 📁 Project Structure

```
tcg-card-layer-generator/
│
├── input/
│   ├── card_base.png          # Base artwork for backsides (place here)
│   └── card_front.png         # Card front for automatic detection (place here)
│
├── output/                    # Generated files (gitignored)
│   ├── layers/                # Print-ready layers
│   └── preview/               # Visual previews
│
├── src/
│   ├── config.py              # All configuration parameters
│   ├── colors.py              # Color theme definitions
│   ├── layers.py              # Core layer generation logic
│   ├── detection.py           # Automatic variant and type detection
│   ├── backside_generator.py  # Backside generator (with variants)
│   └── front_generator.py     # Front generator (automatic detection)
│
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── .gitignore                 # Git ignore rules
```

## 🔧 How It Works

1. **Image Preparation**: Loads base artwork and center-crops to exact card aspect ratio, then resizes to print dimensions
2. **Grayscale Conversion**: Converts to grayscale to extract luminance information
3. **Main Color Layer**: Multiplies grayscale values by theme color, preserving brightness variations
4. **White Layer**: Creates binary mask for areas requiring white ink underprint
5. **Foil Layer**: Creates binary mask for hot foil stamping areas
6. **Spot UV Layer**: Edge detection + morphological operations create emboss/spot UV mask
7. **Preview Generation**: Combines all layers into a 2×2 grid for visual verification

## 🚀 Future Enhancements

Potential additions (not yet implemented):

- ✅ Rainbow gradient support
- ✅ Bleed and crop marks
- ✅ Direct CMYK export
- ✅ PDF/X-4 for print shops
- ✅ Batch processing for multiple cards/themes
- ✅ GUI interface
- ✅ Command-line interface with more options

## 📝 License

[Specify your license here]

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Notes

- The input image should be high-quality for best results
- Layer thresholds can be adjusted in `config.py` based on your artwork characteristics
- All outputs are in PNG format; convert to CMYK/PDF as needed for your printer

---

**Made for professional trading card production** 🎴

