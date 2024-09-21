import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", "bold")
		node2 = TextNode("This is a text node", "bold")
		node3 = TextNode("", "bold")

		self.assertEqual(node, node2)

		self.assertNotEqual(node, node3)

		node4 = TextNode("This is a text node", "")
		node5 = TextNode("This is a text node", "bold", "")
		node6 = TextNode("This is a text node", "italic")

		self.assertNotEqual(node4, node5)
		self.assertNotEqual(node4, node6)

if __name__ == "__main__":
	unittest.main()
