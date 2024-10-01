import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.boot.dev", "target": "_blank"})
        expected = ' href="https://www.boot.dev" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_has_leading_space(self):
        node = HTMLNode(props={"href": "https://www.boot.dev", "target": "_blank"})
        expected = node.props_to_html()
        self.assertTrue(expected.startswith(' '), "Props should start with a leading space")

    def test_props_to_html_attributes_have_spaces(self):
        node = HTMLNode(props={"href": "https://www.boot.dev", "target": "_blank"})
        expected = node.props_to_html()
        self.assertIn(' href=', expected, "There should be a space before 'href'")
        self.assertIn(' target=', expected, "There should be a space before 'target'")

    def test_props_to_html_values_are_quoted(self):
        node = HTMLNode(props={"href": "https://www.boot.dev", "target": "_blank"})
        expected = node.props_to_html()
        self.assertIn('href="', expected, "href value should be in quotes")
        self.assertIn('target="', expected, "target value should be in quotes")

    def test_tag(self):
        tag = "p"
        node = HTMLNode(tag=tag)
        self.assertEqual(node.tag, tag)
    
    def test_value(self):
        value = "Hello, world!"
        node = HTMLNode(value=value)
        self.assertEqual(node.value, value)

    def test_children(self):
        child1 = HTMLNode()
        child2 = HTMLNode()
        parent = HTMLNode(children=[child1, child2])
        self.assertEqual(len(parent.children), 2)
        self.assertIn(child1, parent.children)
        self.assertIn(child2, parent.children)

    def test_children_empty_list(self):
        child1 = HTMLNode()
        child2 = HTMLNode()
        parent = HTMLNode(children=[child1, child2])
        parent2 = HTMLNode(children=[])

        self.assertEqual(len(parent.children), 2)
        self.assertIn(child1, parent.children)
        self.assertIn(child2, parent.children)

        self.assertEqual(len(parent2.children), 0)
        self.assertIsInstance(parent2.children, list)
        self.assertFalse(parent2.children)

    def test_children_default_none(self):
        node = HTMLNode()
        self.assertIsNone(node.children)

    def test_props(self):
        props = {"key": "href", "value": "target"}
        node = HTMLNode(props=props)
        expected = ' key="href" value="target"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode(tag="p", value="Hello, world!", children=None, props={"key": "href", "value": "target"})
        expected = "HTMLNode(p, Hello, world!, children=None, {'key': 'href', 'value': 'target'})"
        self.assertEqual(expected, repr(node))

    def test_HTMLNode_none(self):
        node = HTMLNode()
        expected = "HTMLNode(None, None, children=None, None)"
        self.assertEqual(expected, repr(node))

    def test_HTMLNode_no_tag(self):
        node = HTMLNode(tag=None, value="Hello, world!", children=[],props={"key": "href", "value": "target"})
        expected = "HTMLNode(None, Hello, world!, children=[], {'key': 'href', 'value': 'target'})"
        self.assertEqual(expected, repr(node))

    
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
        print(f"props: {self.props}")
        props_html = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        props_html = f" {props_html}" if props_html else ""
        node = LeafNode(tag=self.tag, value=self.value, props=self.props)
        expected = f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_repr(self):
        node = LeafNode(tag="p", value="Hello, world!", props={"key": "href", "value": "target"})
        expected = "LeafNode(p, Hello, world!, {'key': 'href', 'value': 'target'})"
        self.assertEqual(expected, repr(node))

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

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

    def test_repr(self):
        node = ParentNode(tag="p", children=f"{self.children}", props={"key": "href", "value": "target"})
        expected = "ParentNode(p, children=[LeafNode(b, Bold text, {}), LeafNode(i, italic text, {})], {'key': 'href', 'value': 'target'})"
        self.assertEqual(expected, repr(node))


if __name__ == "__main__":
	unittest.main(exit=False)
