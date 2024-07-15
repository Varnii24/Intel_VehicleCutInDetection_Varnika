import os
import shutil
from sklearn.model_selection import train_test_split

# Define paths
base_path = r"processed_data"
images_root = os.path.join(base_path, "images")
annotations_root = os.path.join(base_path, "labels")
train_images_dir = os.path.join(base_path, "train/images")
val_images_dir = os.path.join(base_path, "val/images")
train_annotations_dir = os.path.join(base_path, "train/labels")
val_annotations_dir = os.path.join(base_path, "val/labels")

# Create train and validation directories if they don't exist
os.makedirs(train_images_dir, exist_ok=True)
os.makedirs(val_images_dir, exist_ok=True)
os.makedirs(train_annotations_dir, exist_ok=True)
os.makedirs(val_annotations_dir, exist_ok=True)

# Function to collect all files in the directory structure
def collect_files(root_dir, extension):
    file_set = set()
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(extension):
                # Store the relative path without the extension
                relative_path = os.path.relpath(os.path.join(root, file), root_dir)
                relative_path = os.path.splitext(relative_path)[0]
                file_set.add(relative_path)
    return list(file_set)

# Collect image and annotation files
image_files = collect_files(images_root, ".jpg")
annotation_files = collect_files(annotations_root, ".txt")

# Ensure both lists contain the same items
image_files.sort()
annotation_files.sort()

# Debugging: Check for mismatches
image_set = set(image_files)
annotation_set = set(annotation_files)

# Files in image_set but not in annotation_set
images_without_annotations = image_set - annotation_set
# Files in annotation_set but not in image_set
annotations_without_images = annotation_set - image_set

if images_without_annotations:
    print("Images without corresponding annotations:")
    for file in images_without_annotations:
        print(file)

if annotations_without_images:
    print("Annotations without corresponding images:")
    for file in annotations_without_images:
        print(file)

# Assert to check if lists match
assert image_files == annotation_files, "Mismatch between image and annotation files."

# Print the number of collected files
print(f"Collected {len(image_files)} image files.")
print(f"Collected {len(annotation_files)} annotation files.")

# Split the data into training and validation sets
train_files, val_files = train_test_split(image_files, test_size=0.2, random_state=42)

# Function to copy files
def copy_files(file_list, source_dir, dest_dir, extension):
    for file in file_list:
        src_file = os.path.join(source_dir, file + extension)
        dest_file = os.path.join(dest_dir, os.path.basename(file) + extension)
        shutil.copy(src_file, dest_file)

# Copy image and annotation files to train and val directories
copy_files(train_files, images_root, train_images_dir, ".jpg")
copy_files(train_files, annotations_root, train_annotations_dir, ".txt")
copy_files(val_files, images_root, val_images_dir, ".jpg")
copy_files(val_files, annotations_root, val_annotations_dir, ".txt")

print("Dataset split into training and validation sets.")
print(f"Training set: {len(train_files)} files")
print(f"Validation set: {len(val_files)} files")
