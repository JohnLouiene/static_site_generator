from enum import Enum
import re
from htmlnode import LeafNode

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

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """Splits up a line of markdown file into a seperate textnodes of a given TextType given a delimiter"""
    #Collection of TextNodes to return
    text_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            text_nodes.append(node)
            continue

        #Collection of texts from the list of old_nodes that are from the text type text
        split_texts = []

        #Split the list of old nodes into text sections
        try:
            split_texts = node.text.split(delimiter)
        except:
            raise ValueError("Invalid delimiter given for stated text type")
        
        #No closing statement
        if len(split_texts) % 2 == 0:
            raise ValueError("Invalid markdown syntax, missing closing delimiter")
        
        for i in range(len(split_texts)):
            if split_texts[i] == "":
                continue
            if i%2 == 0:
                text_nodes.append(TextNode(split_texts[i], TextType.TEXT))
            else:
                text_nodes.append(TextNode(split_texts[i], text_type))

    return text_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """Splits a list of nodes made of lines of markdown files seperating link nodes from the text"""
    #Collection of TextNodes to return
    text_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            text_nodes.append(node)
            continue

        #Split the list of old nodes into text sections
        try:
            md_image_texts = extract_markdown_images(node.text)
            remaining_text = node.text
            for alt, url in md_image_texts:
                md_text = f"![{alt}]({url})"

                split_texts = remaining_text.split(md_text, maxsplit=1)

                before_text = split_texts[0]

                if before_text != "":
                    text_nodes.append(TextNode(before_text, TextType.TEXT))
                
                text_nodes.append(TextNode(alt, TextType.IMAGE, url))

                if len(split_texts) > 1:
                    remaining_text = split_texts[1]

            if remaining_text != "":
                text_nodes.append(TextNode(remaining_text, TextType.TEXT))
        except:
            raise Exception("Error in splitting up text using markdown text for images")

    return text_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """Splits a list of nodes made of lines of markdown files seperating image nodes from the text"""
    #Collection of TextNodes to return
    text_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            text_nodes.append(node)
            continue

        #Split the list of old nodes into text sections
        try:
            md_link_texts = extract_markdown_links(node.text)
            remaining_text = node.text
            for alt, url in md_link_texts:
                md_text = f"[{alt}]({url})"

                split_texts = remaining_text.split(md_text, maxsplit=1)

                before_text = split_texts[0]

                if before_text != "":
                    text_nodes.append(TextNode(before_text, TextType.TEXT))
                
                text_nodes.append(TextNode(alt, TextType.LINK, url))

                if len(split_texts) > 1:
                    remaining_text = split_texts[1]

            if remaining_text != "":
                text_nodes.append(TextNode(remaining_text, TextType.TEXT))
        except:
            raise Exception("Error in splitting up text using markdown text for links")

    return text_nodes

def text_to_textnodes(text) -> list[TextNode]:
    """Converts a markdown file into text nodes with the given text types"""
    text_node_list = [TextNode(text, TextType.TEXT)]
    
    bold_nodes_split = split_nodes_delimiter(text_node_list, "**", TextType.BOLD)
    italic_nodes_split = split_nodes_delimiter(bold_nodes_split, "_", TextType.ITALIC)
    code_nodes_split = split_nodes_delimiter(italic_nodes_split, "`", TextType.CODE)

    image_nodes_split = split_nodes_image(code_nodes_split)
    link_nodes_split = split_nodes_link(image_nodes_split)
    list_text_nodes = link_nodes_split

    return list_text_nodes

def extract_markdown_images(text: str) -> list[str]:
    """Extracts all instances of markdown image texts using regex to a list"""
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[str]:
    """Extracts all instances of markdown link texts using regex to a list"""
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)