import os

# Define the class names and their corresponding integer indices
class_mapping = {
    'bus': 0,
    'rider': 1,
    'autorickshaw': 2,
    'car': 3,
    'person': 4,
    'truck': 5,
    'motorcycle': 6,
    'vehicle_fallback': 7,
    'caravan': 8,
    'train': 9,
    'animal': 10,
    'trailer': 11,
    'traffic_sign': 12,
    'bicycle': 13,
    'traffic_light': 14
}

def rewrite_label_format(annotations_path):
    for root, _, files in os.walk(annotations_path):
        for filename in files:
            if filename.endswith(".txt"):
                filepath = os.path.join(root, filename)
                lines = []
                with open(filepath, 'r') as file:
                    for line in file:
                        parts = line.strip().split()
                        if len(parts) >= 5:  # Check if line has at least 5 parts
                            label1 = parts[0]
                            if len(parts) > 5:
                                label2 = parts[1]
                                xmin = parts[2]
                                ymin = parts[3]
                                xmax = parts[4]
                                ymax = parts[5]
                                new_line = f"{label1}_{label2} {xmin} {ymin} {xmax} {ymax}\n"
                            else:
                                xmin = parts[1]
                                ymin = parts[2]
                                xmax = parts[3]
                                ymax = parts[4]
                                new_line = f"{label1} {xmin} {ymin} {xmax} {ymax}\n"
                            
                            lines.append(new_line)
                        else:
                            print(f"Ignored incorrect format in {filepath}: {line.strip()}")
                
                # Write modified lines back to the file
                with open(filepath, 'w') as file:
                    file.writelines(lines)

def convert_labels_to_integers(filepath):
    lines = []
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 5:
                label = parts[0]
                if label in class_mapping:
                    label_int = class_mapping[label]
                    new_line = f"{label_int} {' '.join(parts[1:])}\n"
                    lines.append(new_line)
                else:
                    print(f"Warning: Label '{label}' not found in class mapping.")
                    lines.append(line)  # Keep original line if label not found in mapping
            else:
                print(f"Warning: Incorrect format in {filepath}: {line.strip()}")
                lines.append(line)  # Keep original line if format is incorrect
    
    # Write modified content back to the file
    with open(filepath, 'w') as file:
        file.writelines(lines)

# Function to process all label files in a directory
def process_label_files(directory):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.txt'):
                filepath = os.path.join(root, filename)
                rewrite_label_format(filepath)  # Rewrite label format first
                convert_labels_to_integers(filepath)  # Convert labels to integers

# Example usage:
annotations_path = 'processed_data\labels'
process_label_files(annotations_path)

print("Label conversion and format rewriting completed.")
