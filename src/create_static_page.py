import os
import shutil
from pathlib import Path
from block_to_html import markdown_to_html_node

def delete_directory(directory_to_remove: str):
    if os.path.exists(directory_to_remove):
        shutil.rmtree(directory_to_remove)

def copy_to_public(origin_path: str, destination_directory: str):
    if not os.path.exists(destination_directory):
        os.mkdir(destination_directory)
            
    files_to_copy = os.listdir(origin_path)

    for file in files_to_copy:
        file_path = os.path.join(origin_path, file)
        new_directory = os.path.join(destination_directory, file)
        print(f" * {file_path} -> {new_directory}")
        if not os.path.isfile(file_path):
            copy_to_public(file_path, new_directory)
        else:
            shutil.copy(file_path, destination_directory)

def extract_title(markdown: str) -> str:
    i = markdown.find("\n")
    if i == -1:
        first_line = markdown
    else:
        first_line = markdown[:i + 1]

    if not first_line.startswith("# "):
        raise Exception("Markdown file must start with an h1 header")

    header = first_line[2::].strip()

    return header

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown_contents = f.read()
    f.close()

    with open(template_path) as f:
        template_contents = f.read()
    f.close()

    content_nodes = markdown_to_html_node(markdown_contents)
    content_html = content_nodes.to_html()

    page_title = extract_title(markdown_contents)

    new_page = template_contents.replace("{{ Title }}", page_title).replace("{{ Content }}", content_html)

    directory_path = os.path.dirname(dest_path)

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    with open(dest_path, "x") as f:
        f.write(new_page)
    f.close()

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    files_to_generate = os.listdir(dir_path_content)

    for file in files_to_generate:
        origin_path = os.path.join(dir_path_content, file)
        destination_path = os.path.join(dest_dir_path, file)
        
        if os.path.isfile(origin_path):
            destination_path = Path(destination_path).with_suffix(".html")
            generate_page(origin_path, template_path, destination_path)
        else:
            generate_pages_recursive(origin_path, template_path, destination_path)
