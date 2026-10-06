import os
from block_converter import markdown_to_blocks
from markdown_to_html import markdown_to_html_node
from htmlnode import *
import re
import sys

basepath = sys.argv[1]

def extract_title(markdown: str) -> str:
    lines = markdown_to_blocks(markdown)

    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("No title found")

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating a page from {from_path} to {dest_path} using {template_path}")

    if not os.path.exists(from_path):
        raise Exception("Source path not found")
      
    with open(from_path, "r") as f:
        md = f.read()
    
    with open(template_path, "r") as f:
        template = f.read()

    node = markdown_to_html_node(md)
    html = node.to_html()
    title = extract_title(md)
    final_html = template.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html)
    final_html = final_html.replace("href=\"/", f"href=\"{basepath}")
    final_html = final_html.replace("src=\"/", f"src=\"{basepath}")


    split_path = dest_path.split("/")
    path_so_far = ""
    for i in range(len(split_path) - 1):
        path_so_far += split_path[i] + "/"
        if not os.path.exists(path_so_far):
            os.mkdir(path_so_far)

    with open(dest_path, "w") as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise Exception("Source path not found")
    elif os.path.isfile(dir_path_content):
        raise Exception("Source path is not a directory")
    
    directory = os.listdir(dir_path_content)
    for item in directory:
        if not os.path.isfile(dir_path_content + str(item)):
            generate_pages_recursive(f"{dir_path_content}{str(item)}/", template_path, f"{dest_dir_path}{str(item)}/")
        elif str(item).endswith(".md"):
            generate_page(f"{dir_path_content}{str(item)}", template_path, f"{dest_dir_path}{str(item[:-3])}.html")
    
