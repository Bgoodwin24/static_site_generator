import unittest
from htmlnode import HTMLNode


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
        expected = "HTMLNode(tag='p', value='Hello, world!', children=None, props={'key': 'href', 'value': 'target'})"
        self.assertEqual(expected, repr(node))

    def test_HTMLNode_none(self):
        node = HTMLNode()
        expected = "HTMLNode(tag=None, value=None, children=None, props=None)"
        self.assertEqual(expected, repr(node))

    def test_HTMLNode_no_tag(self):
        node = HTMLNode(tag=None, value="Hello, world!", props={"key": "href", "value": "target"})
        expected = "HTMLNode(tag=None, value='Hello, world!', children=None, props={'key': 'href', 'value': 'target'})"
        self.assertEqual(expected, repr(node))

if __name__ == "__main__":
	unittest.main(exit=False)
