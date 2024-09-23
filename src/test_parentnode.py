import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def setUp(self):
        self.tag = "p"
        self.children = [
            LeafNode("b", "Bold text"),
            LeafNode("i", "italic text")
        ]

    def test_multiple_children(self):
        node = ParentNode(self.tag, self.children)
        expected ="<p><b>Bold text</b><i>italic text</i></p>"
        self.assertEqual(node.to_html(), expected)


    def test_nested_parent_in_parent(self):
        inner_leaf = LeafNode("b", "Bold text")
        inner_parent = ParentNode("i", [inner_leaf, LeafNode(None, "italic text")])
        outer_parent = ParentNode("p", [inner_parent, LeafNode(None, "Text")])
        expected = "<p><i><b>Bold text</b>italic text</i>Text</p>"
        self.assertEqual(outer_parent.to_html(), expected)


    def test_empty_children(self):
        with self.assertRaises(ValueError) as context:
            ParentNode(tag="p", children=None)

        self.assertEqual(
            str(context.exception),
            "Children are required for a ParentNode and cannot be None."
        )

    def test_no_tags(self):
        with self.assertRaises(ValueError) as context:
            ParentNode(tag=None, children=[])

        self.assertEqual(
            str(context.exception),
            "A tag is required for ParentNode and cannot be None."
        )

    def test_if_value(self):
        with self.assertRaises(TypeError):
            ParentNode(tag="p", value="Unintended value", children=[])

    def test_repr(self):
        node = ParentNode(tag="p", children=f"{self.children}", props={"key": "href", "value": "target"})
        expected = "ParentNode(p, children: [LeafNode(b, Bold text, None), LeafNode(i, italic text, None)], {'key': 'href', 'value': 'target'})"
        self.assertEqual(expected, repr(node))

if __name__ == "__main__":
    unittest.main(exit=False)
