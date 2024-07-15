import os

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

# Example usage:
annotations_path = 'processed_data/labels'
rewrite_label_format(annotations_path)
