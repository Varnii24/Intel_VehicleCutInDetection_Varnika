import os

def find_empty_files(directory):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".txt"):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as file:
                    content = file.read()
                    if content.strip() == "":
                        print(f"Empty file found: {filepath}")



annotations_path = r'processed_data\labels'
find_empty_files(annotations_path)