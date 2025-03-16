import os
import shutil

from static_site_gen.markdownparser import markdown_to_html_node
from static_site_gen.markdownparser import extract_title


def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
    """Generates html pages based on the template by populating it's content from markdown file."""
    print(f"generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as from_file:
        markdown = from_file.read()
    with open(template_path, "r") as template_file:
        template = template_file.read()
    html_obj = markdown_to_html_node(markdown)
    html = html_obj.to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, "w") as dest_file:
        dest_file.write(template)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str
):
    if not os.path.exists(dir_path_content):
        raise Exception("Content directory does not exist.")

    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            dest_path = dest_path.replace(".md", ".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
