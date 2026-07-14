from enum import Enum
from src.htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text: str, text_type: TextType, url:str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
            )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """Converts a text node into an html leaf node"""
    text_type = text_node.text_type
    text_value = text_node.text

    match text_type:
        case TextType.TEXT:
            return LeafNode(None, value=text_value)
        case TextType.BOLD:
            return LeafNode("b", value=text_value)
        case TextType.ITALIC:
            return LeafNode("i", value=text_value)
        case TextType.CODE:
            return LeafNode("code", value=text_value)
        case TextType.LINK:
            return LeafNode("a", value=text_value, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unsupported text type: {text_node.text_type}")
