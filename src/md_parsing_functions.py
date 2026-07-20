import re
from src.textnode import TextNode, TextType

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

def text_to_textnodes(text):
    """Converts a markdown file into text nodes with the given text types"""
    text_node_list = [TextNode(text, TextType.TEXT)]
    
    bold_nodes_split = split_nodes_delimiter(text_node_list, "**", TextType.BOLD)
    italic_nodes_split = split_nodes_delimiter(bold_nodes_split, "_", TextType.ITALIC)
    code_nodes_split = split_nodes_delimiter(italic_nodes_split, "`", TextType.CODE)

    image_nodes_split = split_nodes_image(code_nodes_split)
    link_nodes_split = split_nodes_link(image_nodes_split)

    return link_nodes_split

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
        