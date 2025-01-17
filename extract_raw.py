import os
from easyocr import Reader

# Directories
IMAGE_DIR = '/images'
OUTPUT_DIR = '/images'
MODEL_DIR = '/models'
LANGUAGES = ['en']  # You can add more languages as needed, e.g., ['en', 'fr']

# Ensure the model directory exists
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# Initialize EasyOCR reader with the specified model directory
reader = Reader(LANGUAGES, model_storage_directory=MODEL_DIR)

# Ensure the output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Process each image file in the directory
for filename in os.listdir(IMAGE_DIR):
    filepath = os.path.join(IMAGE_DIR, filename)
    
    # Skip non-image files
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        continue

    print(f"Processing image: {filename}")
    
    # Perform text extraction
    try:
        result = reader.readtext(filepath, detail=0)
        extracted_text = '\n'.join(result)
    except Exception as e:
        print(f"Failed to process {filename}: {e}")
        continue

    # Save the extracted text to a .txt file with the same name as the image
    text_filename = f"{os.path.splitext(filename)[0]}.txt"
    text_filepath = os.path.join(OUTPUT_DIR, text_filename)
    with open(text_filepath, 'w', encoding='utf-8') as text_file:
        text_file.write(extracted_text)
    
    print(f"Text saved to: {text_filepath}")

print("Processing completed.")
