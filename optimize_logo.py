#!/usr/bin/env python3
"""Optimize logo file size while maintaining quality"""

from PIL import Image
import sys

def optimize_logo(input_path, output_path=None, max_size=800):
    """
    Optimize a logo image
    - Resize if too large
    - Convert to optimized format
    - Reduce file size
    """
    if output_path is None:
        output_path = input_path.replace('.png', '-optimized.png')
    
    print(f"Opening: {input_path}")
    img = Image.open(input_path)
    
    print(f"Original size: {img.size[0]}x{img.size[1]} pixels")
    print(f"Original mode: {img.mode}")
    
    # Resize if too large (logos don't need to be huge)
    if img.size[0] > max_size or img.size[1] > max_size:
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        print(f"Resized to: {img.size[0]}x{img.size[1]} pixels")
    
    # Convert RGBA to RGB with white background if needed
    # (saves ~50% file size and works better for print)
    if img.mode in ('RGBA', 'LA'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'RGBA':
            background.paste(img, mask=img.split()[3])  # Alpha channel
        img = background
        print(f"Converted to RGB")
    
    # Save optimized
    img.save(output_path, 'PNG', optimize=True)
    print(f"\n✅ Saved to: {output_path}")
    
    # Show file sizes
    import os
    original_size = os.path.getsize(input_path) / (1024 * 1024)
    new_size = os.path.getsize(output_path) / (1024 * 1024)
    reduction = ((original_size - new_size) / original_size) * 100
    
    print(f"\nOriginal: {original_size:.2f} MB")
    print(f"Optimized: {new_size:.2f} MB")
    print(f"Reduction: {reduction:.1f}%")

if __name__ == '__main__':
    input_file = 'frontend/assets/perfect-dj-logo.png'
    optimize_logo(input_file)
