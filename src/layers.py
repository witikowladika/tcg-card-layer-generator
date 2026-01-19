"""
Layer generation functions for TCG card production.

This module contains all the core image processing logic for creating
print-ready layers from a base artwork.
"""

from PIL import Image, ImageOps, ImageFilter
import numpy as np


def mm_to_px(mm: float, dpi: int) -> int:
    """
    Convert millimeters to pixels at given DPI.
    
    Args:
        mm: Size in millimeters
        dpi: Resolution in dots per inch
        
    Returns:
        Size in pixels (rounded to integer)
    """
    return int(mm / 25.4 * dpi)


def prepare_canvas(img: Image.Image, width_mm: float, height_mm: float, dpi: int) -> Image.Image:
    """
    Prepare input image: crop to exact aspect ratio and resize to target dimensions.
    
    Maintains aspect ratio by center-cropping, then resizes to exact print dimensions.
    
    Args:
        img: Input PIL Image
        width_mm: Target width in millimeters
        height_mm: Target height in millimeters
        dpi: Resolution in dots per inch
        
    Returns:
        Processed PIL Image ready for layer generation
    """
    target_ratio = width_mm / height_mm
    w, h = img.size
    current_ratio = w / h

    # Center crop to match target aspect ratio
    if current_ratio > target_ratio:
        # Image is too wide, crop horizontally
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        # Image is too tall, crop vertically
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))

    # Resize to exact target dimensions
    target_size = (mm_to_px(width_mm, dpi), mm_to_px(height_mm, dpi))
    return img.resize(target_size, Image.LANCZOS)


def generate_main_layer(gray: Image.Image, color: tuple) -> Image.Image:
    """
    Generate main color layer by applying theme color while preserving luminance.
    
    The grayscale image is multiplied by the theme color, preserving
    the original brightness variations.
    
    Args:
        gray: Grayscale PIL Image (mode "L")
        color: RGB tuple (R, G, B) for theme color
        
    Returns:
        Colorized PIL Image (mode "RGB")
    """
    g = np.array(gray)
    out = np.zeros((g.shape[0], g.shape[1], 3), dtype=np.uint8)
    
    for i in range(3):
        out[..., i] = (g / 255.0 * color[i]).astype(np.uint8)
    
    return Image.fromarray(out)


def generate_rainbow_layer(gray: Image.Image, rainbow_colors: list) -> Image.Image:
    """
    Generate rainbow gradient layer by applying color gradient based on horizontal position.
    
    Creates a rainbow effect that transitions through multiple colors based on
    the horizontal position in the image.
    
    Args:
        gray: Grayscale PIL Image (mode "L")
        rainbow_colors: List of RGB tuples for rainbow gradient
        
    Returns:
        Rainbow colorized PIL Image (mode "RGB")
    """
    g = np.array(gray)
    h, w = g.shape
    out = np.zeros((h, w, 3), dtype=np.uint8)
    
    # Create gradient based on horizontal position
    num_colors = len(rainbow_colors)
    
    for x in range(w):
        # Calculate which color segment we're in
        pos = x / w  # 0.0 to 1.0
        segment = pos * (num_colors - 1)
        idx = int(segment)
        t = segment - idx  # Interpolation factor (0.0 to 1.0)
        
        # Handle edge case
        if idx >= num_colors - 1:
            idx = num_colors - 2
            t = 1.0
        
        # Interpolate between two colors
        c1 = np.array(rainbow_colors[idx])
        c2 = np.array(rainbow_colors[idx + 1])
        color = (c1 * (1 - t) + c2 * t).astype(np.uint8)
        
        # Apply color to grayscale values (preserving luminance)
        for y in range(h):
            luminance = g[y, x] / 255.0
            out[y, x] = (color * luminance).astype(np.uint8)
    
    return Image.fromarray(out)


def generate_holo_layer(gray: Image.Image, base_color: tuple) -> Image.Image:
    """
    Generate holographic layer with iridescent effect.
    
    Creates a holo effect by adding color shifts and gradient variations
    to simulate holographic/iridescent appearance.
    
    Args:
        gray: Grayscale PIL Image (mode "L")
        base_color: Base RGB color tuple
        
    Returns:
        Holographic colorized PIL Image (mode "RGB")
    """
    g = np.array(gray)
    h, w = g.shape
    out = np.zeros((h, w, 3), dtype=np.uint8)
    
    # Create holo effect with diagonal gradient and color shifting
    for y in range(h):
        for x in range(w):
            # Create diagonal gradient for holo effect
            diag = (x + y) / (w + h)
            luminance = g[y, x] / 255.0
            
            # Shift colors based on diagonal position (rainbow-like effect)
            angle = diag * 6.28318  # 0 to 2*PI
            
            # Calculate color shift (sine waves for RGB)
            r_shift = np.sin(angle) * 60 + base_color[0]
            g_shift = np.sin(angle + 2.094) * 60 + base_color[1]  # +120 degrees
            b_shift = np.sin(angle + 4.189) * 60 + base_color[2]  # +240 degrees
            
            # Blend with base color
            # NOTE: Use g_val instead of g to avoid overwriting the grayscale array 'g'
            r = int((r_shift * 0.7 + base_color[0] * 0.3) * luminance)
            g_val = int((g_shift * 0.7 + base_color[1] * 0.3) * luminance)
            b = int((b_shift * 0.7 + base_color[2] * 0.3) * luminance)
            
            out[y, x] = [
                max(0, min(255, r)),
                max(0, min(255, g_val)),
                max(0, min(255, b))
            ]
    
    return Image.fromarray(out)


def generate_mask(gray: Image.Image, threshold: int) -> Image.Image:
    """
    Generate binary mask layer based on grayscale threshold.
    
    Pixels above threshold become white (255), below become black (0).
    Used for white ink and foil layers.
    
    Args:
        gray: Grayscale PIL Image (mode "L")
        threshold: Threshold value (0-255)
        
    Returns:
        Binary mask PIL Image (mode "L")
    """
    g = np.array(gray)
    mask = np.where(g > threshold, 255, 0).astype(np.uint8)
    return Image.fromarray(mask, mode="L")


def generate_spot_uv(gray: Image.Image, edge_size: int) -> Image.Image:
    """
    Generate Spot UV / emboss layer from edge detection.
    
    Detects edges in the image and applies morphological operations
    to create printable emboss/spot UV mask.
    
    Args:
        gray: Grayscale PIL Image (mode "L")
        edge_size: Size of edge filter (affects line thickness)
                   Must be odd number >= 3 (will be adjusted if invalid)
        
    Returns:
        Binary mask PIL Image (mode "L") for spot UV printing
    """
    # Ensure filter size is valid (odd number >= 3)
    # MaxFilter requires odd size >= 3
    if edge_size < 3:
        filter_size = 3
    elif edge_size % 2 == 0:  # If even, make it odd
        filter_size = edge_size + 1
    else:
        filter_size = edge_size
    
    # Detect edges
    edges = gray.filter(ImageFilter.FIND_EDGES)
    
    # Dilate edges to make them thicker/printable
    edges = edges.filter(ImageFilter.MaxFilter(filter_size))
    
    # Convert to binary mask
    g = np.array(edges)
    spot_uv = np.where(g > 40, 255, 0).astype(np.uint8)
    
    return Image.fromarray(spot_uv, mode="L")

