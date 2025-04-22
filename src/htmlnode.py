from textnode import TextType

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        """
        tag - A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        value - A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        children - A list of HTMLNode objects representing the children of this node
        props - A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

        An HTMLNode without a tag will just render as raw text
        An HTMLNode without a value will be assumed to have children
        An HTMLNode without children will be assumed to have a value
        An HTMLNode without props simply won't have any attributes
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        # Child classes will override this method to render themselves as HTML.
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props_html_string = ""
        for key, value in self.props.items():
            props_html_string += f' {key}="{value}"'
        return props_html_string
    
    def __repr__(self):
        return f'HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})'

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if not self.value:
            raise ValueError("leaf nodes must have a value")
        
        if not self.tag:
            # if no tag, return value as raw text
            return self.value # value should already be a string
        else:
            # tag looks like (e.g. "p", "a", "h1", etc)
            return f"<{self.tag}{self.props_to_html() if self.props else ""}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if self.children in [[], None]:
            raise ValueError("ParentNode must have children nodes")
        if not isinstance(self.children, list):
            raise ValueError("ParentNode children must come as a list")
        
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, { "href": text_node.url })
        case TextType.IMAGE:
            return LeafNode(
                "img", 
                "", 
                {
                    "src": text_node.url,
                    "alt": text_node.text,
                },
            )
        case _:
            raise ValueError("input text_node does not have valid TextType")
