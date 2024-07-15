import os

# Define paths
annotations_root = "processed_data/annotations"
images_root = "processed_data/images"

# Function to get all files in a directory recursively
def get_all_files(directory, extension):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(extension):
                files.append(os.path.relpath(os.path.join(root, filename), directory))
    return files

# Function to get base filenames without extensions
def get_base_filenames(files, extension):
    base_filenames = {os.path.splitext(file)[0] for file in files if file.endswith(extension)}
    return base_filenames

# Get all annotation and image files recursively
annotation_files = get_all_files(annotations_root, ".txt")
image_files = get_all_files(images_root, ".jpg")

# Get base filenames without extensions
annotation_basenames = get_base_filenames(annotation_files, ".txt")
image_basenames = get_base_filenames(image_files, ".jpg")

# Find extra annotations and images
extra_annotations = annotation_basenames - image_basenames
extra_images = image_basenames - annotation_basenames

# Output the results
print("Extra annotations (without corresponding images):")
for annotation in extra_annotations:
    print(annotation + ".txt")

print("\nExtra images (without corresponding annotations):")
for image in extra_images:
    print(image + ".jpg")

# Delete the extras
for annotation in extra_annotations:
    annotation_path = os.path.join(annotations_root, annotation + ".txt")
    os.remove(annotation_path)
    print(f"Deleted extra annotation: {annotation_path}")

for image in extra_images:
    image_path = os.path.join(images_root, image + ".jpg")
    os.remove(image_path)
    print(f"Deleted extra image: {image_path}")

print("\nExtras deleted.")
