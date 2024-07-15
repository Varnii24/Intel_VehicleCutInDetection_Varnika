import os

# Define paths
images_root = "processed_data/images"
annotations_root = "processed_data/annotations"

# Function to check pairs of image and annotation files
def check_image_annotation_pairs(images_dir, annotations_dir):
    image_files = []
    annotation_files = []

    # Collect all image files
    for root, _, files in os.walk(images_dir):
        for file in files:
            if file.lower().endswith(".jpg"):
                image_files.append(os.path.relpath(os.path.join(root, file), images_dir))

    # Collect all annotation files
    for root, _, files in os.walk(annotations_dir):
        for file in files:
            if file.lower().endswith(".txt"):
                annotation_files.append(os.path.relpath(os.path.join(root, file), annotations_dir))

    # Check pairs
    missing_annotations = []
    for image_file in image_files:
        annotation_file = os.path.join(annotations_dir, os.path.splitext(image_file)[0] + ".txt")
        if annotation_file not in annotation_files:
            missing_annotations.append(image_file)

    return missing_annotations

# Check for missing annotation files corresponding to images
missing_annotations = check_image_annotation_pairs(images_root, annotations_root)

# Output the results
if not missing_annotations:
    print("All images have corresponding annotation files.")
else:
    print("Images missing corresponding annotation files:")
    for image_file in missing_annotations:
        print(image_file)
