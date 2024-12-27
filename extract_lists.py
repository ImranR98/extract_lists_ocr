import os
import sys
import easyocr
import cv2
import numpy as np
from sklearn.cluster import DBSCAN

def preprocess_image(image_path):
    """Load and preprocess the image for better OCR results."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return binary_image

def extract_text(image_path):
    """Extract text from the image using EasyOCR."""
    reader = easyocr.Reader(['en'], download_enabled=True, model_storage_directory='/models', user_network_directory='/models/networks')
    results = reader.readtext(image_path)
    return results

def cluster_and_clean_text(results):
    """Parse and clean OCR results to extract vertical lists of words."""
    boxes = []
    texts = []

    for res in results:
        box, text, _ = res
        texts.append(text)
        # Use the center of the box for clustering
        center_x = (box[0][0] + box[2][0]) / 2
        center_y = (box[0][1] + box[2][1]) / 2
        boxes.append((center_x, center_y))

    boxes = np.array(boxes)

    # Use DBSCAN to cluster words based on their vertical alignment
    clustering = DBSCAN(eps=50, min_samples=1, metric='euclidean').fit(boxes)
    labels = clustering.labels_

    clustered_words = {}
    for label, text in zip(labels, texts):
        if label not in clustered_words:
            clustered_words[label] = []
        clustered_words[label].append(text)

    # Sort words within each cluster by their vertical position (y-coordinate)
    cleaned_lists = []
    for label in sorted(clustered_words):
        sorted_cluster = sorted(
            zip(boxes[labels == label][:, 1], clustered_words[label]), key=lambda x: x[0]
        )
        cleaned_list = [word for _, word in sorted_cluster]
        cleaned_lists.append(cleaned_list)

    return cleaned_lists

def process_folder(folder_path):
    """Process each image in the folder and save results to text files."""
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                # Preprocess the image
                preprocessed_image = preprocess_image(file_path)

                # Extract text from the image
                raw_results = extract_text(preprocessed_image)

                # Save raw OCR results to a text file
                raw_output_file = os.path.join(folder_path, f"{os.path.splitext(file_name)[0]}_raw.txt")
                with open(raw_output_file, "w") as f:
                    for res in raw_results:
                        f.write(f"{res[1]}\n")

                # Parse and clean the OCR results
                lists_of_words = cluster_and_clean_text(raw_results)

                # Save the cleaned lists of words to a text file
                cleaned_output_file = os.path.join(folder_path, f"{os.path.splitext(file_name)[0]}.txt")
                with open(cleaned_output_file, "w") as f:
                    for i, word_list in enumerate(lists_of_words):
                        f.write(f"List {i + 1}: {', '.join(word_list)}\n")

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not os.path.isdir(folder_path):
        print("The specified path is not a folder.")
        sys.exit(1)

    try:
        process_folder(folder_path)
        print("Processing completed. Results saved in the same folder as the images.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
