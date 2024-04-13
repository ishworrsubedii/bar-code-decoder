import os

# Define the directories
image_dir = '/resources/dataset/dataset/images'
label_dir = 'dataset/archive/labels'

# Get the list of files in both directories
image_files = os.listdir(image_dir)
label_files = os.listdir(label_dir)

# Check for .txt files in both directories
common_files = [file for file in image_files if file.endswith('.txt') and file in label_files]

# Find image files without corresponding label files and vice versa
image_without_label = [file for file in image_files if file not in label_files]
label_without_image = [file for file in label_files if file not in image_files]

# Remove image files without corresponding label files and vice versa
for file in image_without_label:
    os.remove(os.path.join(image_dir, file))
    print(f'Removed image file without label: {file}')

for file in label_without_image:
    os.remove(os.path.join(label_dir, file))
    print(f'Removed label file without image: {file}')

# Print the result
if common_files:
    print("The following .txt files are present in both directories:")
    for file in common_files:
        print(file)
else:
    print("No .txt files are common in both directories.")
