from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            removed_syntax = node.text.split(delimiter)
            if len(removed_syntax) % 2 != 1:
                raise Exception("Invalid syntax: Missing closing delimiter")

            for i in range(len(removed_syntax)):
                if removed_syntax[i] == "":
                    continue
                if i % 2 == 0 and removed_syntax[i] != "":
                    new_node = TextNode(removed_syntax[i], TextType.TEXT)
                else:
                    new_node = TextNode(removed_syntax[i], text_type)
                    
                new_nodes.append(new_node)
    
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    
def extract_markdown_links(text: str) -> list[tuple]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        original_text = node.text
        links = extract_markdown_images(original_text)
        if links == [] and original_text != "":
            new_nodes.append(node)
        else:
            for link in links:
                image_alt = link[0]
                image_link = link[1]
                sections = original_text.split(f"![{image_alt}]({image_link})", 1)
                original_text = sections[1]
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            if original_text != "":
                new_nodes.append(TextNode(original_text, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        original_text = node.text
        links = extract_markdown_links(original_text)
        if links == [] and original_text != "":
            new_nodes.append(node)
        else:
            for link in links:
                link_alt = link[0]
                text_link = link[1]
                sections = original_text.split(f"[{link_alt}]({text_link})", 1)
                original_text = sections[1]
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(link_alt, TextType.LINK, text_link))
            if original_text != "":
                new_nodes.append(TextNode(original_text, TextType.TEXT))
    
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    node = TextNode(text, TextType.TEXT)
    nodes = [node]
    delimiters = {"**" : TextType.BOLD, "_" : TextType.ITALIC, "`" : TextType.CODE}

    for key in delimiters:
        nodes = split_nodes_delimiter(nodes, key, delimiters[key])
    
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes