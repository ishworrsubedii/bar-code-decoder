"""
Created By: ishwor subedi
Date: 2024-04-13
"""
"""
Created By: ishwor subedi
Date: 2024-04-13
"""
import os

# Define the directory
dir_path = '/resources/dataset/dataset/labels/'

# Get the list of .txt files in the directory
txt_files = [file for file in os.listdir(dir_path) if file.endswith('.txt')]

# Iterate over each .txt file
for file in txt_files:
    with open(os.path.join(dir_path, file), 'r') as f:
        lines = f.readlines()

    # Remove lines where the first word is '1'
    lines = [line for line in lines if not line.split()[0] == '4']

    # Write the remaining lines back to the file
    with open(os.path.join(dir_path, file), 'w') as f:
        f.writelines(lines)

    print(f'Processed file: {file}')