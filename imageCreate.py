from PIL import Image

def create_colored_box_image(color, filename):
    img = Image.new('RGBA', (20, 20), color)
    img.save(f'assets/{filename}')

# Define colors
colors = {
    'fatal': (139, 0, 0),   # rgba(139, 0, 0, 0.5)
    'serious': (255, 0, 0), # rgba(255, 0, 0, 0.5)
    'slight': (255, 159, 0) # rgba(255, 159, 0, 0.5)
}

# Create images for each severity level
create_colored_box_image(colors['fatal'], 'fatal.png')
create_colored_box_image(colors['serious'], 'serious.png')
create_colored_box_image(colors['slight'], 'slight.png')