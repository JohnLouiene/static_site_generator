from create_static_page import copy_to_public, delete_directory, generate_pages_recursive

def main():
    markdown_files = "../content"
    static_contents = "../static"
    template_to_use = "../template.html"
    destination_folder = "../public"

    delete_directory(destination_folder)
    copy_to_public(static_contents, destination_folder)
    generate_pages_recursive(markdown_files, template_to_use, destination_folder)

main()