import os
import zipfile

def unzip_files_in_directory(directory_path):
    """
    Unzips each .zip file in the specified directory into a separate folder named after the file.

    Args:
    directory_path (str): The path to the directory containing the .zip files.
    """
    # Iterate over all the items in the directory
    for item in os.listdir(directory_path):
        # Construct the full path to the item
        full_item_path = os.path.join(directory_path, item)
        
        # Check if the item is a file and has a .zip extension
        if os.path.isfile(full_item_path) and item.endswith('.zip'):
            # Create a directory name by removing the .zip extension from the file name
            directory_name = item[:-4]
            full_directory_path = os.path.join(directory_path, directory_name)
            
            # Create the directory if it doesn't exist
            if not os.path.exists(full_directory_path):
                os.makedirs(full_directory_path)
            
            # Open the zip file and extract all its contents into the newly created directory
            with zipfile.ZipFile(full_item_path, 'r') as zip_ref:
                zip_ref.extractall(full_directory_path)
            print(f"Extracted {item} into {full_directory_path}")

# Example usage
# Replace '/path/to/your/directory' with the actual path to the directory containing your zip files
unzip_files_in_directory('../../parsed')