from htmlnode import ParentNode, HTMLNode
from textblocks import BlockType, markdown_to_blocks, block_to_block_type
from textnode import TextNode, TextType, text_node_to_html_node, text_to_textnodes

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    parent_block_node = ParentNode("div", children=[])

    for block in blocks:
        block_type = block_to_block_type(block)
        parent_node = block_to_HTML_node(block, block_type)

        parent_block_node.children.append(parent_node)

    return parent_block_node

def block_to_HTML_node(block: str, block_type = BlockType) -> HTMLNode:
    match block_type:
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.HEADING:
            return header_to_html_node(block)
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case _:
            raise ValueError("Invalid or unrecognized block type entered")

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes = []

    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))

    return html_nodes

def quote_to_html_node(text: str) -> HTMLNode:
    lines = text.split('\n')
    new_text = ""

    for line in lines:
        new_line = ""

        if line.startswith("> "):
            new_line = line.removeprefix("> ")
        elif line.startswith(">"):
            new_line = line.removeprefix(">")

        if new_line != "":
            new_text += new_line + " "

    new_text = new_text[:-1]
    children = text_to_children(new_text)

    return ParentNode("blockquote", children)

def unordered_list_to_html_node(text: str) -> HTMLNode:
    lines = text.split('\n')
    children = []

    for line in lines:
        new_line = line.removeprefix("- ")
        list_node = ParentNode("li", children=text_to_children(new_line))
        children.append(list_node)

    return ParentNode("ul", children)

def ordered_list_to_html_node(text: str) -> HTMLNode:
    lines = text.split('\n')
    children = []

    i = 1
    for line in lines:
        new_line = line.removeprefix(f"{i}. ")
        list_node = ParentNode("li", children=text_to_children(new_line))
        children.append(list_node)
        i += 1

    return ParentNode("ol", children=children)

def code_to_html_node(text: str) -> HTMLNode:
    if not text.startswith("```\n") or not text.endswith("```"):
        raise ValueError("Invalid code block")
    
    new_text = text.lstrip()
    new_text = new_text[4:-3]

    text_node = TextNode(new_text, TextType.TEXT)
    child = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [child])

    return ParentNode("pre", children=[code_node])

def header_to_html_node(text: str) -> HTMLNode:
    i = 0
    while i < len(text) and i < 6 and text[i] == "#":
        i += 1

    prefix = "#" * i + " "
    new_text = text.removeprefix(prefix)

    return ParentNode(tag=f"h{i}", children=text_to_children(new_text))

def remove_newlines(text: str) -> str:
    return text.replace("\n", " ")

def paragraph_to_html_node(text: str) -> HTMLNode:
    #Note double or single backticks seem to be stripped
    new_text = remove_newlines(text)
    return ParentNode("p", children=text_to_children(new_text))