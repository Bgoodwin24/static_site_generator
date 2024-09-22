from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        self.tag = tag
        self.value = value
        self.props = props
        if value is None:
            raise ValueError("Value is required for a LeafNode and cannot be None.")
        if props is None:
            props = {}

        super().__init__(tag=tag, value=value, props=props or {})

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode must have a non-empty value.")
        
        props_html = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        props_html = f" {props_html}" if props_html else ""
        
        if self.tag == None:
            return self.value

        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
