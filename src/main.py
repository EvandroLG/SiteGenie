import os
import shutil
import logging

from inline_markdown import extract_title
from io_utils import read_file
from markdown_blocks import markdown_to_html_node

def main():
    copy_files("static", "public")
    generate_pages_from_directory("content", "template.html", "public")

def generate_pages_from_directory(directory, template_path, target_directory):
    for file in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, file)):
            generate_pages_from_directory(os.path.join(directory, file), template_path, os.path.join(target_directory, file))
        elif file.endswith(".md"):
            from_path = os.path.join(directory, file)
            generate_page(from_path, template_path, target_directory)

def generate_page(from_path, template_path, to_path):
    print(f"Generating page from {from_path} to {to_path} using {template_path}")

    markdown = read_file(from_path)
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = (read_file(template_path)
                    .replace("{{ Title }}", title)
                    .replace("{{ Content }}", html))

    if not os.path.isdir(to_path):
        os.makedirs(to_path)


    file = os.path.join(to_path, from_path.split("/")[-1]).replace(".md", ".html")

    with open(file, "w") as file:
        file.write(template)

def copy_files(source, target):
    logging.info(f"Copying files from {source} to {target}")

    shutil.rmtree(target, ignore_errors=True)

    def helper(src, dst):
        entries = os.listdir(src)

        for entry in entries:
            source_path = os.path.join(src, entry)
            target_path = os.path.join(dst, entry)

            if os.path.isdir(source_path):
                os.makedirs(target_path, exist_ok=True)
                helper(source_path, target_path)
            else:
                shutil.copy(source_path, target_path)

    helper(source, target)

if __name__ == "__main__":
    main()
