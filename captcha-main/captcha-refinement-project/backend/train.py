import random
import string
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import tensorflow as tf
from tensorflow.keras import layers, models

# Function to generate CAPTCHA image
def generate_captcha_image(captcha_text):
    # Create a blank image
    image = Image.new('RGB', (200, 50), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # Use a font to draw the CAPTCHA text
    try:
        font = ImageFont.truetype("arial.ttf", 24)  # Ensure the font file is available
    except IOError:
        font = ImageFont.load_default()
    
    draw.text((10, 10), captcha_text, font=font, fill=(0, 0, 0))
    
    # Save the image to a bytes buffer
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    
    return buffer

# Generate synthetic CAPTCHA data
def generate_synthetic_data(num_samples=1000, captcha_length=6):
    X = []
    y = []
    characters = string.ascii_uppercase + string.digits  # All possible characters
    for _ in range(num_samples):
        captcha_text = ''.join(random.choices(characters, k=captcha_length))
        image = generate_captcha_image(captcha_text)
        image = Image.open(image).convert('L')  # Convert to grayscale
        image = image.resize((100, 30))  # Resize to a fixed size
        X.append(np.array(image))
        y.append(captcha_text)
    return np.array(X), np.array(y)

# Create a character-to-index mapping
def create_char_to_index_mapping():
    characters = string.ascii_uppercase + string.digits  # 26 letters + 10 digits
    return {char: idx for idx, char in enumerate(characters)}

# Convert CAPTCHA text to one-hot encoded labels
def captcha_to_one_hot(captcha_text, char_to_index, captcha_length=6):
    num_classes = len(char_to_index)
    one_hot = np.zeros((captcha_length, num_classes))
    for i, char in enumerate(captcha_text):
        one_hot[i, char_to_index[char]] = 1
    return one_hot

# Build the CNN model
def build_model(input_shape, num_classes, captcha_length=6):
    input_layer = layers.Input(shape=input_shape)
    x = layers.Conv2D(32, (3, 3), activation='relu')(input_layer)
    x = layers.MaxPooling2D((2, 2))(x)
    x = layers.Conv2D(64, (3, 3), activation='relu')(x)
    x = layers.MaxPooling2D((2, 2))(x)
    x = layers.Flatten()(x)
    x = layers.Dense(128, activation='relu')(x)
    
    # Output layer for each character in the CAPTCHA
    outputs = []
    for _ in range(captcha_length):
        outputs.append(layers.Dense(num_classes, activation='softmax')(x))
    
    model = models.Model(inputs=input_layer, outputs=outputs)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Generate synthetic data
X, y = generate_synthetic_data()

# Preprocess data
X = X / 255.0  # Normalize pixel values
X = np.expand_dims(X, axis=-1)  # Add channel dimension (for grayscale images)

# Create character-to-index mapping
char_to_index = create_char_to_index_mapping()

# Convert CAPTCHA labels to one-hot encoded format
y_one_hot = np.array([captcha_to_one_hot(captcha_text, char_to_index) for captcha_text in y])

# Split one-hot encoded labels into separate arrays for each character
y_split = [y_one_hot[:, i, :] for i in range(y_one_hot.shape[1])]

# Train the model
model = build_model(input_shape=(30, 100, 1), num_classes=len(char_to_index))
model.fit(X, y_split, epochs=10, batch_size=32)  # Train the model with the synthetic data

# Save the model
model.save('captcha_model.h5')
