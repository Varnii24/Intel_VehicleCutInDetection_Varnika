import os

# Define paths
annotations_path = "processed_data/labels"
images_path = "processed_data/images"

# Function to count all files in a directory recursively
def count_files(directory, extension=None):
    count = 0
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if extension is None or filename.endswith(extension):
                count += 1
    return count

# Count files in the specified directories
annotation_file_count = count_files(annotations_path)
image_file_count = count_files(images_path)

# Output the counts
print(f"Total number of annotation files in '{annotations_path}': {annotation_file_count}")
print(f"Total number of image files in '{images_path}': {image_file_count}")
