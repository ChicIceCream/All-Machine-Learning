import json
import os

# Specify the path to your JSON file
json_file_path = 'notebook_json.json'  # Update this with the correct path to your JSON file

# Load the JSON content
with open(json_file_path, 'r') as f:
    notebook_content = json.load(f)

# Extract the cells
cells = notebook_content['cells']

# Initialize an empty string to store the Python code
python_code = ""

# Loop through each cell and concatenate the code cells
for cell in cells:
    if cell['cell_type'] == 'code':
        python_code += ''.join(cell['source']) + '\n\n'

# Specify the output Python file path
python_file_path = 'converted_notebook.py'

# Write the concatenated code to a .py file
with open(python_file_path, 'w') as f:
    f.write(python_code)

print(f"Notebook has been successfully converted to {python_file_path}")
