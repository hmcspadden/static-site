from block_converter import *
from inline_converter import *
from textnode import *
from htmlnode import *


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    final_nodes = []
    for node in text_nodes:
        final_nodes.append(text_node_to_html_node(node))
    
    return final_nodes


def heading_to_html(text: str) -> ParentNode:
    heading_size = 0
    for char in text:
        if char == " ":
            break
        heading_size += 1
    
    text = text[heading_size + 1:]
    tag = "h" + str(heading_size)
    children = text_to_children(text)

    return ParentNode(tag=tag, children=children)


def quote_to_html(text: str) -> ParentNode:
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        if line.startswith("> "):
            new_lines.append(line[2:])
        else:
            new_lines.append(line[1:])
    text = "<br />".join(new_lines)
    children = text_to_children(text)

    return ParentNode(tag="blockquote", children=children)


def list_to_html(text: str, trim: int) -> list[HTMLNode]:
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        children = text_to_children(line[trim:])
        new_lines.append(ParentNode("li", children))

    return new_lines


def unordered_to_html(text: str) -> ParentNode:
    children = list_to_html(text, 2)

    return ParentNode(tag="ul", children=children)


def ordered_to_html(text: str) -> ParentNode:
    children = list_to_html(text, 3)

    return ParentNode(tag="ol", children=children)


def code_to_html(text: str) -> LeafNode:
    text = text[3:]
    text = text[:-3]
    code_node = TextNode(text, TextType.CODE)
    child = text_node_to_html_node(code_node)

    return ParentNode(tag="pre", children=[child])


def paragraph_to_html(text: str) -> ParentNode:
    lines = text.split("\n")
    text = " ".join(lines)
    children = text_to_children(text)

    return ParentNode(tag="p", children=children)


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type is BlockType.HEADING:
            children.append(heading_to_html(block))
        elif block_type is BlockType.QUOTE:
            children.append(quote_to_html(block))
        elif block_type is BlockType.UNORDERED_LIST:
            children.append(unordered_to_html(block))
        elif block_type is BlockType.ORDERED_LIST:
            children.append(ordered_to_html(block))
        elif block_type is BlockType.CODE:
            children.append(code_to_html(block))
        else:
            children.append(paragraph_to_html(block))
    
    return ParentNode(tag="div", children=children)

