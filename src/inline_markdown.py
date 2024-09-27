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
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid Markdown Syntax: Missing closing delimiter for '{delimiter}'")
            
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    image_extracted = re.findall (r"!\[([\w\s]*?)\]\((.*?)\)", text)
    return image_extracted

def extract_markdown_links(text):
    link_extracted = re.findall (r"(?<!!)\[([^\]]*?)\]\((.*?)\)", text)
    return link_extracted

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        current_text = old_node.text
        images = extract_markdown_images(current_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for image in images:
            sections = current_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
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

        current_text = old_node.text
        links = extract_markdown_links(current_text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = current_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            current_text = sections[1]
        if current_text != "":
            new_nodes.append(TextNode(current_text, text_type_text))
    return new_nodes
