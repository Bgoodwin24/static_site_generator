import unittest

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


if __name__ == "__main__":
	unittest.main(exit=False)
