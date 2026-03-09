#!/usr/bin/env python3
"""
Script to create a simple automation-themed .ico file for the application.
Creates a multi-size icon with 16x16, 32x32, 48x48, and 256x256 sizes.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create a multi-size automation-themed icon."""
    
    # Icon sizes to generate
    sizes = [(16, 16), (32, 32), (48, 48), (256, 256)]
    images = []
    
    for size in sizes:
        # Create image with transparent background
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw a simple mouse cursor icon (automation theme)
        width, height = size
        center_x, center_y = width // 2, height // 2
        
        # Mouse pointer shape
        if size[0] >= 32:
            # Draw a more detailed mouse pointer for larger sizes
            points = [
                (center_x - width//6, center_y - height//4),
                (center_x + width//6, center_y - height//4),
                (center_x + width//8, center_y + height//4),
                (center_x, center_y + height//3),
                (center_x - width//8, center_y + height//4)
            ]
            draw.polygon(points, fill=(70, 130, 180, 255), outline=(50, 100, 150, 255))
            
            # Add a keyboard key accent
            key_size = width // 6
            key_x = center_x + width//4
            key_y = center_y - height//6
            draw.rectangle([key_x, key_y, key_x + key_size, key_y + key_size], 
                          fill=(100, 149, 237, 255), outline=(70, 130, 180, 255))
        else:
            # Simple arrow for small sizes
            points = [
                (center_x - 3, center_y - 3),
                (center_x + 3, center_y),
                (center_x - 3, center_y + 3),
                (center_x - 1, center_y)
            ]
            draw.polygon(points, fill=(70, 130, 180, 255))
        
        images.append(img)
    
    # Create assets directory if it doesn't exist
    os.makedirs('assets', exist_ok=True)
    
    # Save as multi-size ICO file
    icon_path = 'assets/app.ico'
    images[0].save(icon_path, format='ICO', sizes=[(img.width, img.height) for img in images])
    
    print(f"✓ Icon created at {icon_path}")
    print(f"  Sizes: {', '.join([f'{w}x{h}' for w, h in sizes])}")
    return icon_path

if __name__ == '__main__':
    create_icon()
