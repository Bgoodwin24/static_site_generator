import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_value_req(self):
        with self.assertRaises(ValueError):
            LeafNode(None)

    def test_tag_no_props(self):
        node = LeafNode("p", "Hello")
        expected = "<p>Hello</p>"
        self.assertEqual(node.to_html(), expected)

    def test_tag_multi_props(self):
        node = LeafNode("a", "Link", {"href": "https://www.boot.dev", "target": "Example"})
        expected = '<a href="https://www.boot.dev" target="Example">Link</a>'
        self.assertEqual(node.to_html(), expected)

    def test_tag_is_none(self):
        node = LeafNode(value=str)
        expected = str
        self.assertEqual(node.to_html(), expected)

if __name__ == "__main__":
    unittest.main(exit=False)
