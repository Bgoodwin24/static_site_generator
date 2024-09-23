import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_value_req(self):
        with self.assertRaises(ValueError):
            LeafNode(self.tag, value=None)

    def test_tag_no_props(self):
        node = LeafNode("p", "Hello")
        expected = "<p>Hello</p>"
        self.assertEqual(node.to_html(), expected)

    def test_tag_multi_props(self):
        node = LeafNode("a", "Link", {"href": "https://www.boot.dev", "target": "Example"})
        expected = '<a href="https://www.boot.dev" target="Example">Link</a>'
        self.assertEqual(node.to_html(), expected)

    def test_tag_is_none(self):
        node = LeafNode(tag=None, value=str)
        expected = str
        self.assertEqual(node.to_html(), expected)

    def setUp(self):
        self.tag = "a"
        self.value = "Link"
        self.props = {"href": "https://www.boot.dev"}

    def test_leaf_to_html(self):
        props_html = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        props_html = f" {props_html}" if props_html else ""
        node = LeafNode(tag=self.tag, value=self.value, props=self.props)
        expected = f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
        self.assertEqual(node.to_html(), expected)

    def test_repr(self):
        node = LeafNode(tag="p", value="Hello, world!", props={"key": "href", "value": "target"})
        expected = "LeafNode(p, Hello, world!, {'key': 'href', 'value': 'target'})"
        self.assertEqual(expected, repr(node))

if __name__ == "__main__":
    unittest.main(exit=False)
