import sys
import os
from create_static_page import copy_to_directory, delete_directory, generate_pages_recursive

def main():
    markdown_files = os.environ["MARKDOWN_FILES"]
    static_contents = os.environ["STATIC_CONTENTS"]
    template_to_use = os.environ["TEMPLATE_TO_USE"]
    destination_folder = os.environ["DESTINATION_FOLDER"]

    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "/"

    delete_directory(destination_folder)
    copy_to_directory(static_contents, destination_folder)
    generate_pages_recursive(markdown_files, template_to_use, destination_folder, base_path)

main()