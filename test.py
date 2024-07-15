import os

def delete_files_with_outside_range_coordinates(annotations_path):
    files_to_delete = []
    
    for root, dirs, files in os.walk(annotations_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                issues_found = False
                
                with open(file_path, 'r') as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) >= 5:
                            xmin = float(parts[1])
                            ymin = float(parts[2])
                            xmax = float(parts[3])
                            ymax = float(parts[4])
                            
                            if xmin < 0 or ymin < 0 or xmax > 1 or ymax > 1:
                                issues_found = True
                                break
                                
                if issues_found:
                    files_to_delete.append(file_path)
    
    if files_to_delete:
        print("Deleting files with coordinates outside the range [0, 1]:")
        for file_path in files_to_delete:
            try:
                image_file = os.path.splitext(file_path)[0] + '.jpg'
                os.remove(file_path)
                os.remove(image_file)
                print(f"Deleted: {file_path}")
                print(f"Deleted: {image_file}")
            except Exception as e:
                print(f"Error deleting files: {e}")
    else:
        print("No files found with coordinates outside the range [0, 1].")

# Run the function to delete problematic files
delete_files_with_outside_range_coordinates(r'processed_data/train/labels')
delete_files_with_outside_range_coordinates(r'processed_data/val/labels')
