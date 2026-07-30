from static_to_public import copy_to_public, delete_directory, generate_page

def main():
    static_directory = "../static"
    public_directory = "../public"

    delete_directory(public_directory)
    copy_to_public(static_directory, public_directory)
    generate_page("../content/index.md", "../template.html", "../public/index.html")

main()