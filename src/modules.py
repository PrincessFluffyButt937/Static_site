
from pathlib import Path
import os, shutil
from functions import extract_title
from htmlnode import markdown_to_html_node, LeafNode, ParentNode

def public_clear(public="/home/art/projects/static_site/Static_site/public"):
    shutil.rmtree(public)

def re_copy(source="/home/art/projects/static_site/Static_site/static", target="/home/art/projects/static_site/Static_site/public"):
    if not os.path.exists(target):
        os.makedirs(target)
    files = os.listdir(source)
    if not files:
        return
    dir_list = []
    tar_dict = {}
    for file in files:
        source_path = os.path.join(source, file)
        target_path = os.path.join(target, file)
        if os.path.isfile(source_path):
            shutil.copy(source_path, target)
            continue
        tar_dict[target_path] = source_path
        dir_list.append(target_path)
        os.makedirs(target_path)
    if not dir_list:
        return
    else:
        for directory in dir_list:
            src_path = tar_dict[directory]
            re_copy(src_path, directory)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    markdown_parrent = markdown_to_html_node(markdown_content)
    title = extract_title(markdown_content)
    html_str = markdown_parrent.to_html()

    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html_str)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)