import re
from textnode import (
    TextNode,
    text_type_text,
	text_type_bold,
	text_type_italic,
	text_type_code,
	text_type_link,
	text_type_image,
)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    split_nodes = []
    list_item = "* "
    for old_node in old_nodes:
        split_nodes = []
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        if delimiter == list_item and old_node.text.startswith(delimiter):
            list_content = old_node.text[2:]
            split_nodes.append(TextNode(list_content, text_type_text))
        else:
            sections = old_node.text.split(delimiter)

        if delimiter != list_item and len(sections) % 2 == 0:
            raise ValueError(f"Invalid Markdown Syntax: Missing closing delimiter for '{delimiter}'")
            
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 != 0:
                split_nodes.append(TextNode(sections[i], text_type))
            else:
                split_nodes.append(TextNode(sections[i], text_type_text))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    image_extracted = re.findall (r"!\[([\w\s]*?)\]\((.*?)\)", text)
    return image_extracted

def extract_markdown_links(text):
    link_extracted = re.findall (r"(?<!!)\[([^\]]*?)\]\((.*?)\)", text)
    return link_extracted

def is_markdown_well_formed(text):
    stack = []

    for char in text:
        if char in ['[', '(']:
            stack.append(char)
        elif char == ']':
            if not stack or stack[-1] != '[':
                return False
            stack.pop()
        elif char == ')':
            if not stack or stack[-1] != '(':
                return False
            stack.pop()

    return not stack

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        if not is_markdown_well_formed(old_node.text):
            raise ValueError("Invalid markdown, image section not closed")

        current_text = old_node.text
        images = extract_markdown_images(current_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for image in images:
            sections = current_text.split(f"![{image[0]}]({image[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(
                TextNode(
                    image[0],
                    text_type_image,
                    image[1],
                )
            )
            current_text = sections[1]

        if current_text != "":
            new_nodes.append(TextNode(current_text, text_type_text))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        if not is_markdown_well_formed(old_node.text):
            raise ValueError("Invalid markdown, link section not closed")

        current_text = old_node.text
        links = extract_markdown_links(current_text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = current_text.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            current_text = sections[1]
        if current_text != "":
            new_nodes.append(TextNode(current_text, text_type_text))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
