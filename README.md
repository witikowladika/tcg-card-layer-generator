# TCG Card Layer Generator

A professional Python tool to generate print-ready layers for trading cards from a single high-quality base artwork. Designed for Pokémon-style cards with support for white ink, foil stamping, and spot UV effects.

## ✨ Features

- **Exact Aspect Ratio Preservation** - Maintains precise 63×88 mm card dimensions
- **Parametric Recoloring** - Apply any theme color while preserving luminance details
- **Print-Ready Layer Separation**:
  - Main color layer (CMYK-ready artwork)
  - White ink layer (underprinting mask)
  - Foil layer (hot foil stamping mask)
  - Spot UV / emboss layer (glossy finish mask)
- **Visual Preview Generation** - 2×2 grid showing all layers side-by-side
- **Pokémon-Style Color Themes** - Pre-configured color palettes for all types

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
```bash
python src/main.py
```

This will generate layers using the default "grass" theme.

### Using Different Color Themes

Specify a theme as a command-line argument:

```bash
python src/main.py fire
python src/main.py water
python src/main.py lightning
```

Available themes:
- `grass` - Green (default)
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

### Output Structure

After running, you'll find:

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
python src/main.py custom_theme
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
│   └── card_base.png          # Your base artwork (place here)
│
├── output/                    # Generated files (gitignored)
│   ├── layers/                # Print-ready layers
│   └── preview/               # Visual previews
│
├── src/
│   ├── config.py              # All configuration parameters
│   ├── colors.py              # Color theme definitions
│   ├── layers.py              # Core layer generation logic
│   └── main.py                # Entry point
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

