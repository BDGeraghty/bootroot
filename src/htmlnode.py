

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("This method should be implemented in subclasses")
    
    def props_to_html(self):
        return ' '.join(f'{key}="{value}"' for key, value in self.props.items()) if self.props else ''
    
    def add_child(self, child):
        self.children.append(child)

    def to_string(self):
        props = ' '.join(f'{key}="{value}"' for key, value in self.props.items())
        props_str = f' {props}' if props else ''
        children_str = ''.join(child.to_string() if isinstance(child, HTMLNode) else str(child) for child in self.children)
        return f'<{self.tag}{props_str}>{children_str}</{self.tag}>'

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children})"
    



class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if not self.children:
            raise ValueError("invalid HTML: no children")
        return f"<{self.tag}{self.props_to_html()}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.value}, {self.children}, {self.props})"
