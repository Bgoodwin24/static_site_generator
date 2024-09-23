from htmlnode import HTMLNode
from leafnode import LeafNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("A tag is required for ParentNode and cannot be None.")
        if children is None:
            raise ValueError("Children are required for a ParentNode and cannot be None.")
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("A tag is required for ParentNode and cannot be None.")
        if not self.children:
            raise ValueError("Children are required for a ParentNode and cannot be None.")

        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
