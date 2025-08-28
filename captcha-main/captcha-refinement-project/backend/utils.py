import random
import string
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import os

def generate_captcha_image(captcha_text):
    """Generates a CAPTCHA image with noise, distortions, and lines."""
    
    width, height = 200, 50
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Load Font
    try:
        font_path = os.path.join(os.path.dirname(__file__), "data", "arial.ttf")
        font = ImageFont.truetype(font_path, 30)
    except IOError:
        font = ImageFont.load_default()

    # Random position for text
    text_x = random.randint(10, 30)
    text_y = random.randint(5, 15)

    # Draw text with a slight rotation for distortion
    draw.text((text_x, text_y), captcha_text, font=font, fill=(0, 0, 0))

    # Add random lines
    for _ in range(5):  # Adjust the number of lines
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        draw.line(((x1, y1), (x2, y2)), fill=(0, 0, 0), width=2)

    # Add random noise (dots)
    for _ in range(100):  # Increase or decrease noise density
        x, y = random.randint(0, width), random.randint(0, height)
        draw.point((x, y), fill=(random.randint(0, 150), random.randint(0, 150), random.randint(0, 150)))

    # Apply a slight blur to make OCR detection harder
    image = image.filter(ImageFilter.GaussianBlur(radius=0.7))

    # Save the image to a bytes buffer
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer
