import os
import cv2
import numpy as np
import xml.etree.ElementTree as ET
from tqdm import tqdm

# Define paths
images_path = "dataset/images"
annotations_path = "dataset/annotations"
output_images_path = "processed_data/images"
output_annotations_path = "processed_data/annotations"

# Create output directories if they don't exist
os.makedirs(output_images_path, exist_ok=True)
os.makedirs(output_annotations_path, exist_ok=True)

def preprocess_image(image_path, output_path):
    image = cv2.imread(image_path)
    # Resize image to a fixed size (e.g., 640x480)
    resized_image = cv2.resize(image, (640, 480))
    cv2.imwrite(output_path, resized_image)

def preprocess_annotation(annotation_path, output_path, image_width, image_height):
    if not os.path.exists(annotation_path):
        print(f"Annotation file {annotation_path} not found. Skipping.")
        return False
    
    tree = ET.parse(annotation_path)
    root = tree.getroot()
    annotations = []

    for obj in root.findall('object'):
        name = obj.find('name').text
        bndbox = obj.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)
        
        # Normalize coordinates to range [0, 1]
        xmin_norm = xmin / image_width
        ymin_norm = ymin / image_height
        xmax_norm = xmax / image_width
        ymax_norm = ymax / image_height
        
        annotations.append(f"{name} {xmin_norm} {ymin_norm} {xmax_norm} {ymax_norm}")

    # Save annotations to txt file in YOLO format or any required format
    with open(output_path, 'w') as file:
        for annotation in annotations:
            file.write(annotation + '\n')
    return True

# Process all images and annotations
for subdir in os.listdir(images_path):
    subdir_path = os.path.join(images_path, subdir)
    if os.path.isdir(subdir_path):
        for root, _, files in os.walk(subdir_path):
            for file in tqdm(files):
                if file.endswith(".jpg"):
                    image_path = os.path.join(root, file)
                    relative_path = os.path.relpath(image_path, images_path)
                    output_image_path = os.path.join(output_images_path, relative_path)
                    output_annotation_path = os.path.join(output_annotations_path, relative_path.replace(".jpg", ".txt"))

                    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
                    os.makedirs(os.path.dirname(output_annotation_path), exist_ok=True)

                    # Get image dimensions for annotation normalization
                    image = cv2.imread(image_path)
                    image_height, image_width, _ = image.shape

                    preprocess_image(image_path, output_image_path)
                    annotation_path = os.path.join(annotations_path, relative_path.replace(".jpg", ".xml"))
                    if not preprocess_annotation(annotation_path, output_annotation_path, image_width, image_height):
                        print(f"Skipping image {image_path} due to missing annotation.")

print("Preprocessing complete.")
