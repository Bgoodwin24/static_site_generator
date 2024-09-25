import unittest

from split_nodes_delimiter import *
from htmlnode import LeafNode
from textnode import (
    TextNode,
    text_type_text,
	text_type_bold,
	text_type_italic,
	text_type_code,
	text_type_link,
	text_type_image,
    text_node_to_html_node,
)


class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", text_type_text)
		node2 = TextNode("This is a text node", text_type_text)
		self.assertEqual(node, node2)

	def test_eq_false(self):
		node = TextNode("This is a text node", text_type_text)
		node2 = TextNode("This is a text node", text_type_bold)
		self.assertNotEqual(node, node2)
	
	def test_eq_false2(self):
		node = TextNode("This is a text node", text_type_text)
		node2 = TextNode("This is a text node2", text_type_text)
		self.assertNotEqual(node, node2)
	
	def test_eq_url(self):
		node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
		node2 = TextNode(
			"This is a text node", text_type_text, "https://www.boot.dev"
		)
		self.assertEqual(node, node2)

	def test_repr(self):
		node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
		self.assertEqual(
			"TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
		)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_text(self):
        text_node = TextNode("text", text_type_text)
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.tag, None)
        self.assertEqual(result.value, "text")

    def test_text_node_bold(self):
        text_node = TextNode("bold", text_type_bold)
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.tag, "b")
        self.assertEqual(result.value, "bold")

    def test_text_node_italic(self):
        text_node = TextNode("italic", text_type_italic)
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.tag, "i")
        self.assertEqual(result.value, "italic")

    def test_text_node_code(self):
        text_node = TextNode("code", text_type_code)
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.tag, "code")
        self.assertEqual(result.value, "code")

    def test_text_node_link(self):
        text_node = TextNode("link", text_type_link, text_type_link)
        result = text_node_to_html_node(text_node)
        expected = LeafNode("a", "link", {"href": text_node.url})
        self.assertEqual(result, expected)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.tag, "a")
        self.assertEqual(result.value, "link", {"href": text_type_link})
        self.assertEqual(result.props["href"], text_node.url)

    def test_text_node_image(self):
        text_node = TextNode("image", text_type_image, {"src": text_type_link, "alt": text_type_text})
        result = text_node_to_html_node(text_node)
        expected = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        self.assertEqual(result, expected)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.tag, "img")
        self.assertEqual(result.value, "")
        self.assertEqual(result.props, {"src": text_node.url, "alt": text_node.text})

class TestSplitDelimiter(unittest.TestCase):
    def test_text_basic(self):
        node = [TextNode("This is text", text_type_text)]
        expected = [TextNode("This is text", text_type_text)]
        self.assertListEqual(node, expected)

    def test_text_bold(self):
        node = TextNode("This is **bold** text", text_type_text)
        result = split_nodes_delimiter([node], "**", text_type_bold)
        expected = [
              TextNode("This is ", text_type_text),
              TextNode("bold", text_type_bold),
              TextNode(" text", text_type_text),
        ]
        self.assertListEqual(result, expected)

    def test_text_italic(self):
        node = TextNode("This is *italic* text", text_type_text)
        result = split_nodes_delimiter([node], "*", text_type_italic)
        expected = [
              TextNode("This is ", text_type_text),
              TextNode("italic", text_type_italic),
              TextNode(" text", text_type_text),
        ]
        self.assertListEqual(result, expected)

    def test_text_code(self):
        node = TextNode("This is `code` text", text_type_text)
        result = split_nodes_delimiter([node], "`", text_type_code)
        expected = [
              TextNode("This is ", text_type_text),
              TextNode("code", text_type_code),
              TextNode(" text", text_type_text),
        ]
        self.assertListEqual(result, expected)

    #def test_text_link(self):
        #node = "This is [link] text", text_type_text
        #result = split_nodes_delimiter([node], "()", text_type_link)
        #expected = [
                #TextNode("This is ", text_type_text),
                #TextNode("link", text_type_link),
                #TextNode(" text", text_type_text),
        #]
        #self.assertListEqual(node, expected)

    #def test_text_image(self):
         #node = "This is ![image](https://www.boot.dev) text", text_type_text
         #result = split_nodes_delimiter([node], "![]()", text_type_image)
         #expected = [
                # TextNode("This is , text_type_text"),
                # TextNode("image", text_type_image),
                # TextNode(" text", text_type_text),
                #]
         #self.assertListEqual(node, expected)

    def test_unmatched_delimiter(self):
        node = TextNode("This is unmatched **bold text", text_type_text)
        delimiter = "**"
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "**", text_type_bold)

        expected_message = f"Invalid Markdown Syntax: Missing closing delimiter for '{delimiter}'"
        self.assertEqual(str(context.exception), expected_message)

    def test_text_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
        self.assertListEqual(
            [
               TextNode("bold", text_type_bold),
               TextNode(" and ", text_type_text),
               TextNode("italic", text_type_italic),
            ],
            new_nodes,
         )
    
    def test_text_bold_double(self):
        node = TextNode(
             "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
             [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
             ],
             new_nodes,
        )

    def test_text_bold_multiword(self):
        node = TextNode(
             "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

if __name__ == "__main__":
	unittest.main(exit=False)
