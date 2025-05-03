from textnode import *
from modules import *

dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    print("Deleting public directory...")
    public_clear()
    print("Copying static files to public directory...")
    re_copy()
    print("Generating page...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)

main()
