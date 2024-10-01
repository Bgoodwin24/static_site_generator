import unittest
from htmlnode import HTMLNode, LeafNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes
from block_markdown import markdown_to_blocks, block_to_block_type, markdown_to_html_node, text_to_children

class TestBlockMarkdown(unittest.TestCase):
    def test_block_markdown(self):
        text = "This is a heading""\n\n""This is a paragraph of text. It has some **bold** and *italic* words inside of it.""\n\n""* This is the first list item in a list block""\n""* This is a list item""\n""* This is another list item"
        node = markdown_to_blocks(text)
        expected = [
            "This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        self.assertEqual(node, expected)
    
    def test_leading_and_trailing_spaces(self):
        text = " This is a heading ""\n\n"" This is a paragraph of text. It has some **bold** and *italic* words inside of it.""\n\n"" * This is the first list item in a list block ""\n"" * This is a list item ""\n"" * This is another list item "
        node = markdown_to_blocks(text)
        expected = [
            "This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        self.assertEqual(node, expected)

    def test_empty_block_strip(self):
        text = "This is a heading""\n\n""This is a paragraph of text. It has some **bold** and *italic* words inside of it.""\n\n""* This is the first list item in a list block""\n""* This is a list item""\n\n\n"
        node = markdown_to_blocks(text)
        expected = [
            "This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item"
        ]
        self.assertEqual(node, expected)

class TestBlocktoBlockType(unittest.TestCase):
    def test_paragraph_type(self):
        text = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        block = block_to_block_type(text)
        expected = "Paragraph"
        self.assertEqual(block, expected)
    
    def test_heading_type_1(self):
        text = "# Heading 1"
        block = block_to_block_type(text)
        expected = "Heading"
        self.assertEqual(block, expected)

    def test_heading_type_6(self):
        text = "###### Heading 6"
        block = block_to_block_type(text)
        expected = "Heading"
        self.assertEqual(block, expected)
    
    def test_code_type(self):
        text = "```\nCode\n```"
        block = block_to_block_type(text)
        expected = "Code"
        self.assertEqual(block, expected)

    def test_quote_type(self):
        text = "> Quote"
        block = block_to_block_type(text)
        expected = "Quote"
        self.assertEqual(block, expected)

    def test_unordered_list_asterisk_type(self):
        text = "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        block = block_to_block_type(text)
        expected = "Unordered List"
        self.assertEqual(block, expected)

    def test_unordered_list_dash_type(self):
        text = "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        block = block_to_block_type(text)
        expected = "Unordered List"
        self.assertEqual(block, expected)

    def test_ordered_type(self):
        text = "1. This is the first list item in a list block\n2. This is a list item\n3. This is another list item"
        block = block_to_block_type(text)
        expected = "Ordered List"
        self.assertEqual(block, expected)

class TestMarkdownToHtml(unittest.TestCase):
    @staticmethod
    def create_html_node(tag, contents, children=None):
        if children is None:
            return HTMLNode(tag, contents)
        return HTMLNode(tag, contents, children)
    
    def test_md_to_html(self):
        text = (
            "# This is a heading\n\n"
            "This is a paragraph of text.\n\n"
            "> This is a quote\n\n"
            "```\nThis is code\n```\n\n"
            "* This is the first list item in a list block\n"
            "* This is a list item\n"
            "* This is another list item\n\n"
            "1. This is the first list item in a list block\n"
            "2. This is a list item\n"
            "3. This is another list item"
        )
        html_node = markdown_to_html_node(text)
        expected_children = [
            self.create_html_node("h1", "This is a heading"),
            self.create_html_node("p", "This is a paragraph of text."),
            self.create_html_node("blockquote", None, children=[self.create_html_node(None, "This is a quote")]),
            self.create_html_node("pre", None, children=[
                self.create_html_node("code", "This is code")
            ]),
            self.create_html_node("ul", None, children=[
                self.create_html_node("li", "This is the first list item in a list block"),
                self.create_html_node("li", "This is a list item"),
                self.create_html_node("li", "This is another list item")
            ]),
            self.create_html_node("ol", None, children=[
                self.create_html_node("li", "This is the first list item in a list block"),
                self.create_html_node("li", "This is a list item"),
                self.create_html_node("li", "This is another list item")
            ])
        ]
        expected = self.create_html_node("div", None, children=expected_children)
        self.assertEqual(html_node, expected)


if __name__ == "__main__":
    unittest.main(exit=False)
