"""
Automatic detection functions for Pokémon card fronts.

Detects card variant (shiny/holo/normal) and type (grass, fire, etc.)
based on image analysis.
"""

import numpy as np
from PIL import Image
from colors import POKEMON_COLORS


def detect_variant(img: Image.Image) -> str:
    """
    Detect card variant (shiny, holo, rainbow, or normal) based on edge patterns.
    
    Pokémon cards typically have:
    - Rainbow: Extreme color variance with many unique colors across all edges
    - Holo: Rainbow/holographic shimmer effect visible at edges (high color variance)
    - Shiny: Distinct border pattern/stripes around edges with high contrast
    - Normal: Plain borders with consistent colors
    
    Args:
        img: RGB PIL Image
        
    Returns:
        Variant string: "shiny", "holo", "rainbow", or "normal"
    """
    w, h = img.size
    img_np = np.array(img)
    
    # Analyze edge regions (typically 5-8% of image size for border detection)
    edge_width = max(5, int(min(w, h) * 0.06))
    
    # Extract edge regions (top, bottom, left, right)
    top_edge = img_np[0:edge_width, :, :]
    bottom_edge = img_np[h-edge_width:h, :, :]
    left_edge = img_np[:, 0:edge_width, :]
    right_edge = img_np[:, w-edge_width:w, :]
    
    # Combine all edges
    edges = np.concatenate([
        top_edge.reshape(-1, 3),
        bottom_edge.reshape(-1, 3),
        left_edge.reshape(-1, 3),
        right_edge.reshape(-1, 3)
    ], axis=0)
    
    # Calculate per-channel variance in edges
    r_var = np.var(edges[:, 0])
    g_var = np.var(edges[:, 1])
    b_var = np.var(edges[:, 2])
    edge_variance = (r_var + g_var + b_var) / 3.0
    
    # Calculate color variance across all channels (holo has high variance due to rainbow)
    channel_means = np.mean(edges, axis=0)
    color_variance = np.var(channel_means)
    
    # Calculate saturation in edges (shiny has higher saturation)
    max_rgb = np.max(edges, axis=1)
    min_rgb = np.min(edges, axis=1)
    saturation = np.where(max_rgb > 0, (max_rgb - min_rgb) / max_rgb, 0)
    avg_saturation = np.mean(saturation)
    
    # Calculate brightness variance (shiny has distinct bright patterns)
    brightness = np.mean(edges, axis=1)
    brightness_variance = np.var(brightness)
    brightness_std = np.std(brightness)
    
    # Calculate contrast (difference between max and min brightness in edges)
    max_brightness = np.max(brightness)
    min_brightness = np.min(brightness)
    contrast = max_brightness - min_brightness
    
    # Detection thresholds (tuned for typical Pokémon card patterns)
    
    # Check for rainbow pattern first (extreme variance across all channels, all edges)
    # Rainbow cards have very high variance everywhere, not just edges
    if edge_variance > 5000 and color_variance > 4000:
        # Additional check: rainbow often has all colors present
        edge_colors_unique = len(np.unique(edges.reshape(-1, 3), axis=0))
        if edge_colors_unique > 100:  # Many unique colors = rainbow effect
            return "rainbow"
    
    # Holo: Very high color variance in edges (rainbow/holographic effect)
    # High variance across all RGB channels indicates rainbow effect
    if edge_variance > 3500 or color_variance > 3000:
        return "holo"
    
    # Shiny: High saturation, high brightness variance/contrast (distinct border patterns)
    # Shiny cards have bright, saturated borders with high contrast
    if (avg_saturation > 0.35 and brightness_variance > 1200) or contrast > 180:
        return "shiny"
    
    # Normal: Default (low variance, consistent colors)
    return "normal"


def detect_type(img: Image.Image) -> str:
    """
    Detect card type by analyzing dominant color in inner region.
    
    Crops out edges and analyzes the center region to find the dominant
    color, then matches it to the closest Pokémon type color.
    
    Uses HSV color space for better perceptual matching, especially to
    distinguish water (blue) from metal (gray).
    
    Args:
        img: RGB PIL Image
        
    Returns:
        Type string: "grass", "fire", "water", etc.
    """
    w, h = img.size
    img_np = np.array(img)
    
    # Crop inner region (exclude 10% edge on all sides)
    crop_margin = int(min(w, h) * 0.10)
    inner = img_np[crop_margin:h-crop_margin, crop_margin:w-crop_margin, :]
    
    # Calculate average color in inner region
    avg_color = np.mean(inner.reshape(-1, 3), axis=0).astype(int)
    avg_r, avg_g, avg_b = avg_color
    
    # Convert average color to HSV for better perceptual matching
    from colorsys import rgb_to_hsv
    avg_h, avg_s, avg_v = rgb_to_hsv(avg_r / 255.0, avg_g / 255.0, avg_b / 255.0)
    
    # Special handling: If image has blue hue and some saturation, strongly prefer water over metal
    # Blue hue range: approximately 0.5 to 0.7 in HSV (240° to 180° in degrees, but normalized 0-1)
    is_blue_hue = (avg_h >= 0.45 and avg_h <= 0.75) and avg_s > 0.15
    
    # Find closest matching Pokémon type color
    min_distance = float('inf')
    best_match = "grass"  # Default
    
    for type_name, type_color in POKEMON_COLORS.items():
        # Convert type color to HSV
        type_h, type_s, type_v = rgb_to_hsv(
            type_color[0] / 255.0,
            type_color[1] / 255.0,
            type_color[2] / 255.0
        )
        
        # Special case: If we detect blue hue, heavily penalize metal
        if is_blue_hue and type_name == "metal":
            # Add large penalty to metal when we have a blue-ish image
            distance = float('inf')
        elif not is_blue_hue and type_name == "water" and avg_s < 0.1:
            # If image is very desaturated (gray), penalize water slightly
            distance = float('inf')
        else:
            # Calculate distance in HSV space with weighted components
            # Hue is most important for distinguishing colors (e.g., blue vs gray)
            # Use circular distance for hue (0 and 1 are close)
            hue_diff = abs(avg_h - type_h)
            hue_distance = min(hue_diff, 1.0 - hue_diff)  # Circular distance
            
            # Weighted distance: hue is most important (3x), saturation (1.5x), value (1x)
            hsv_distance = (
                hue_distance * 3.0 +
                abs(avg_s - type_s) * 1.5 +
                abs(avg_v - type_v) * 1.0
            )
            
            # Also calculate RGB distance as a fallback for very desaturated colors
            rgb_distance = np.sqrt(
                (avg_r - type_color[0]) ** 2 +
                (avg_g - type_color[1]) ** 2 +
                (avg_b - type_color[2]) ** 2
            )
            
            # For very low saturation colors (grays), prefer RGB distance
            # For colored images, prefer HSV distance
            if avg_s < 0.1:
                # Very desaturated (grayish) - use RGB distance
                distance = rgb_distance
            else:
                # Colored image - use HSV distance, but also consider RGB as tiebreaker
                distance = hsv_distance * 50.0 + rgb_distance * 0.1
        
        if distance < min_distance:
            min_distance = distance
            best_match = type_name
    
    return best_match


def calculate_color_distance(color1: tuple, color2: tuple) -> float:
    """
    Calculate Euclidean distance between two RGB colors.
    
    Args:
        color1: RGB tuple (R, G, B)
        color2: RGB tuple (R, G, B)
        
    Returns:
        Distance value (lower = more similar)
    """
    return np.sqrt(
        (color1[0] - color2[0]) ** 2 +
        (color1[1] - color2[1]) ** 2 +
        (color1[2] - color2[2]) ** 2
    )

