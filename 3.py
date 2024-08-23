

import os
import sys

def transform_string(input_string):
    # Split the string by underscores
    parts = input_string.split('_')
    
    # Join the first two parts back together with an underscore
    result = '_'.join(parts[:2])
    
    return result

def cleanup_and_rename():
    # Define the directory path
    directory = r'C:\Users\user\Desktop\Somdeb\coupling\odb_vtk'

    # Iterate over all the files in the directory
    for filename in os.listdir(directory):
        # Get the full file path
        file_path = os.path.join(directory, filename)
        
        # Check if the file is not a .pvtu or .vtu file and if it is a file (not a directory)
        if os.path.isfile(file_path) and not (filename.endswith('.pvtu') or filename.endswith('.vtu')):
            try:
                # Remove the file
                os.remove(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

    # Rename the .pvtu file to match the base name of the .vtk file
    for filename in os.listdir(directory):
        if filename.endswith('.pvtu'):
            old_file_path = os.path.join(directory, filename)
            new_file_name = transform_string(filename) + '.pvtu'
            new_file_path = os.path.join(directory, new_file_name)
            try:
                os.rename(old_file_path, new_file_path)
            except Exception as e:
                print('already exists!')

def remove_extra_pvtu(directory):
    # Iterate over all the files in the directory
    for filename in os.listdir(directory):
        # Check if the file ends with `.pvtu`
        if filename.endswith('.pvtu'):
            old_file_path = os.path.join(directory, filename)
            
            # Remove all redundant `.pvtu` extensions
            new_file_name = filename
            while new_file_name.endswith('.pvtu'):
                new_file_name = new_file_name[:-5]  # Remove last '.pvtu'
            
            # Append single '.pvtu' to the cleaned file name
            new_file_name += '.pvtu'
            new_file_path = os.path.join(directory, new_file_name)
            
            # Rename the file if the new file name is different
            if old_file_path != new_file_path:
                try:
                    os.rename(old_file_path, new_file_path)
                    # print(f'Renamed file: {old_file_path} to {new_file_path}')
                except Exception as e:
                    print('lol!')

if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print("Usage: python 3.py <vtk_file_path>")
    #     sys.exit(1)
    
    cleanup_and_rename()
    directory = r'C:\Users\user\Desktop\Somdeb\coupling\odb_vtk'  # Define your directory path here
    remove_extra_pvtu(directory)
    # remove_extra_pvtu()
