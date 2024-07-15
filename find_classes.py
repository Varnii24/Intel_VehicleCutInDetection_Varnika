#finding classes

import os

# Define the annotations path
annotations_path = r"processed_data/labels"

# Function to extract class names from annotation files
def get_class_names(annotations_path):
    class_names = set()
    for root, _, files in os.walk(annotations_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        for line in f:
                            if len(line.strip()) == 0:
                                continue
                            class_name = line.split()[0]
                            class_names.add(class_name)
                    # Debugging information
                    print(f"Processed file: {file_path}")
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
    return list(class_names)

# Get class names
class_names = get_class_names(annotations_path)
print("Class names:", class_names)
print("Number of classes:", len(class_names))