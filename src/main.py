from static_to_public import copy_to_public, delete_directory

def main():
    delete_directory("../public")
    copy_to_public()

main()