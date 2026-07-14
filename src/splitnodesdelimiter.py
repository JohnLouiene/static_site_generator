from enum import Enum
from src.textnode import TextNode, TextType

class DelimiterType(Enum):
    BOLD = "**"
    ITALIC = "_"
    CODE = "`"

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """Converts a line of markdown file into a textnode given a delimiter from DelimiterType"""
    #Collection of TextNodes to return
    text_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            text_nodes.append(node)
            continue

        #Collection of texts from the list of old_nodes that are from the text type text
        split_text = []

        #Split the list of old nodes into text sections
        try:
            split_text = node.text.split(delimiter)
        except:
            raise ValueError("Invalid delimiter given for stated text type")
        
        #No closing statement
        if len(split_text) % 2 == 0:
            raise ValueError("Invalid markdown syntax, missing closing delimiter")
        
        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i%2 == 0:
                text_nodes.append(TextNode(split_text[i], TextType.TEXT))
            else:
                text_nodes.append(TextNode(split_text[i], text_type))

    return text_nodes

        