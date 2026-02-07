from PIL import Image, ImageDraw
import os

# Create app icon (256x256)
icon_sizes = [(16, 16), (32, 32), (64, 64), (128, 128), (256, 256)]

for size in icon_sizes:
    img = Image.new('RGBA', size, (0, 100, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw a circle (like arc reactor)
    center = (size[0]//2, size[1]//2)
    radius = min(size)//3
    draw.ellipse([center[0]-radius, center[1]-radius, 
                  center[0]+radius, center[1]+radius], 
                 fill=(0, 200, 255, 255))
    
    # Draw J in the center
    from PIL import ImageFont
    try:
        font = ImageFont.truetype("Arial", size[1]//3)
    except:
        font = ImageFont.load_default()
    
    # Save
    img.save(f'jarvis_icon_{size[0]}.png')
    print(f"Created icon: jarvis_icon_{size[0]}.png")

print("\n✅ Icons created!")
