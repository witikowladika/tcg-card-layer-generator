"""
Pokémon-style color theme definitions.

Each color is defined as RGB tuples (R, G, B) with values 0-255.
These colors are used to recolor the base artwork while preserving
the original grayscale luminance values.
"""

POKEMON_COLORS = {
    "grass": (78, 159, 61),
    "fire": (201, 55, 55),
    "water": (60, 120, 216),
    "lightning": (240, 200, 40),
    "psychic": (170, 70, 180),
    "fighting": (150, 80, 50),
    "darkness": (40, 40, 40),
    "metal": (180, 180, 180),
    "dragon": (90, 140, 60),
    "fairy": (240, 160, 200),
    "colorless": (210, 210, 210),
}

def get_shiny_color(base_color: tuple) -> tuple:
    """
    Generate shiny version of a color (brighter, more saturated).
    
    Args:
        base_color: Base RGB color tuple
        
    Returns:
        Shiny RGB color tuple
    """
    r, g, b = base_color
    # Increase brightness and saturation
    # Brighten by 20% and increase saturation
    r = min(255, int(r * 1.2) + 20)
    g = min(255, int(g * 1.2) + 20)
    b = min(255, int(b * 1.2) + 20)
    return (r, g, b)

# Rainbow colors in order for gradient generation
RAINBOW_COLORS = [
    (201, 55, 55),    # Red (fire)
    (240, 200, 40),   # Yellow (lightning)
    (78, 159, 61),    # Green (grass)
    (60, 120, 216),   # Blue (water)
    (170, 70, 180),   # Purple (psychic)
    (240, 160, 200),  # Pink (fairy)
]

def get_color(theme: str) -> tuple:
    """
    Get color tuple for a given theme.
    
    Args:
        theme: Color theme name (e.g., "grass", "fire")
        
    Returns:
        RGB tuple (R, G, B)
        
    Raises:
        KeyError: If theme is not found
    """
    if theme not in POKEMON_COLORS:
        available = ", ".join(POKEMON_COLORS.keys())
        raise KeyError(
            f"Unknown theme '{theme}'. Available themes: {available}"
        )
    return POKEMON_COLORS[theme]

