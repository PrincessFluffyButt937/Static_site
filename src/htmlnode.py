

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("HTML node does not have to_html method")
    
    def props_to_html(self):
        if isinstance(self.props, dict):
            return "".join([f' {key}="{value}"' for key, value in self.props.items()if isinstance(key, str) and isinstance(value, str)])
        return ""
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode cannot have value = None")
        if self.tag == None:
            return self.value
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("In PattentNode, Tag cannot be None.")
        if self.children == None:
            raise ValueError("Children is None.")
        else:
            html = f"<{self.tag}{self.props_to_html()}>"

            for child in self.children:
                html += child.to_html()
        
            html += f"</{self.tag}>"

            return html