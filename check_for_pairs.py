import os

# Define paths
images_root = r"processed_data/images"
annotations_root = r"processed_data/annotations"

# Function to collect all files in the directory structure
def collect_files(root_dir, extension):
    file_set = set()
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(extension):
                file_set.add(os.path.join(root, file))  # Collect full paths
    return file_set

# Collect image and annotation files with full paths
image_files = collect_files(images_root, ".jpg")
annotation_files = collect_files(annotations_root, ".txt")

# Identify mismatches
missing_annotations = []
missing_images = []

for image_file in image_files:
    annotation_file = image_file.replace(".jpg", ".txt")
    if annotation_file not in annotation_files:
        missing_annotations.append(annotation_file)

for annotation_file in annotation_files:
    image_file = annotation_file.replace(".txt", ".jpg")
    if image_file not in image_files:
        missing_images.append(image_file)

# Output the results
print(f"Total image files: {len(image_files)}")
print(f"Total annotation files: {len(annotation_files)}")

if not missing_annotations and not missing_images:
    print("All images have corresponding annotation files and vice versa.")
else:
    if missing_annotations:
        print("\nImages missing corresponding annotation files:")
        for image in missing_annotations:
            print(image)

    if missing_images:
        print("\nAnnotations missing corresponding image files:")
        for annotation in missing_images:
            print(annotation)
