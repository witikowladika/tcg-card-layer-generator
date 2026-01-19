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
        
    Returns:
        Binary mask PIL Image (mode "L") for spot UV printing
    """
    # Detect edges
    edges = gray.filter(ImageFilter.FIND_EDGES)
    
    # Dilate edges to make them thicker/printable
    edges = edges.filter(ImageFilter.MaxFilter(edge_size))
    
    # Convert to binary mask
    g = np.array(edges)
    spot_uv = np.where(g > 40, 255, 0).astype(np.uint8)
    
    return Image.fromarray(spot_uv, mode="L")

