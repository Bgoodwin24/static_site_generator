import re
from textnode import (
    TextNode, 
    text_node_to_html_node, 
    text_type_text, 
    text_type_bold,
	text_type_italic,
	text_type_code,
	text_type_link,
	text_type_image,
)
from htmlnode import HTMLNode, LeafNode

def markdown_to_blocks(markdown):
    block_list = []
    current_block = []
    split_markdown = markdown.split("\n")
    for line in split_markdown:
        if line != "":
            current_block.append(line.strip())
        if line == "" and current_block != []:
            block_list.append("\n".join(current_block))
            current_block = []
    if current_block != []:
        block_list.append("\n".join(current_block))
    return block_list

def block_to_block_type(block):
    heading = r"^#+\s"
    code = "```"
    ordered_list = r"^\d+\.\s"
    lines = block.split("\n")

    if re.match(heading, lines[0]):
        return "Heading"
    if lines[0].startswith(code) and lines[-1].startswith(code):
        return "Code"
    if all(line.startswith("> ") for line in lines):
            return "Quote"
    if all(line.startswith("* ") or line.startswith("- ") for line in lines):
        return "Unordered List"
    if all(re.match(ordered_list, line) for line in lines):
        return "Ordered List"
    else:
        return "Paragraph"

def text_to_children(text):
    return [HTMLNode(value=text.strip(), children=[], props=None)]

def markdown_to_html_node(markdown):
    block_list = []
    parent = HTMLNode("div", value=None, children=block_list, props=None)
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == "Paragraph":
            text = block.strip()
            block_list.append(HTMLNode("p", text, children=[], props=None))

        if block_type == "Heading":
            count = sum(1 for char in block if char == "#")
            heading_content = block[count:].strip()
            block_list.append(HTMLNode(f"h{count}", value=heading_content, children=[], props=None))

        if block_type == "Code":
            code_lines = block.splitlines()
            joined_code = "\n".join(code_lines[1:-1])
            code_node = HTMLNode("code", value=joined_code, children=[], props=None)
            block_list.append(HTMLNode("pre", children=[code_node], props=None))

        if block_type == "Quote":
            quote_content = "\n".join(line.lstrip("> ").strip() for line in block.splitlines())
            text_value = text_to_children(quote_content)
            block_list.append(HTMLNode("blockquote", children=text_value, props=None))

        if block_type == "Unordered List":
            list_items = []
            for item in block.splitlines():
                clean_item = item[2:].strip()
                list_items.append(HTMLNode("li", value=clean_item, props=None))
            block_list.append(HTMLNode("ul", children=list_items, props=None))

        if block_type == "Ordered List":
            list_items = []
            for item in block.splitlines():
                clean_item = item.split(" ", 1)[1]
                list_items.append(HTMLNode("li", value=clean_item.strip(), props=None))
            block_list.append(HTMLNode("ol", children=list_items, props=None))
    return parent
