import os
import shutil

def delete_directory(directory_to_remove: str):
    if os.path.exists(directory_to_remove):
        shutil.rmtree(directory_to_remove)

def copy_to_public(origin_path: str = "../static", destination_directory: str = "../public"):
    if not os.path.exists(destination_directory):
        os.mkdir(destination_directory)
            
    files_to_copy = os.listdir(origin_path)

    for file in files_to_copy:
        file_path = os.path.join(origin_path, file)

        if not os.path.isfile(file_path):
            new_directory = os.path.join(destination_directory, file)
            copy_to_public(file_path, new_directory)
        else:
            shutil.copy(file_path, destination_directory)
        

