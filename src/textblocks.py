from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    """Splits a markdown file into a list of text blocks given they have newline spacing"""
    blocks = markdown.split("\n\n")
    result = []

    for block in blocks:
        stripped_block = block.strip()

        if stripped_block != '':
            result.append(stripped_block)

    return result

def block_to_block_type(block: str) -> BlockType:
    """Checks the block type of a markdown text block"""

    if block.startswith(("# ","## ","### ","#### ","##### ","###### ")):
        prefix = ""
        i = 0

        while i < len(block) and block[i] == "#":
            prefix += block[i]
            i += 1

        prefix += " "

        if len(block) > len(prefix) and block[len(prefix)::].strip() != "":
            return BlockType.HEADING
    
    if block.startswith(("```\n")) and block[:-4:-1] == "```":
        return BlockType.CODE
    
    if block.startswith(">") and len(block) > 1:
        lines = block.split("\n")
        is_quote = True
        for line in lines:
            if not line.startswith(">"):
                is_quote = False
                break
        if is_quote:
            return BlockType.QUOTE
    
    if block.startswith("- "):
        lines = block.split("\n")
        is_unordered_list = True
        for line in lines:
            if not line.startswith("- "):
                is_unordered_list = False
                break
        if is_unordered_list:
            return BlockType.UNORDERED_LIST
        
    if block.startswith("1. "):
        lines = block.split("\n")
        is_ordered_list = True
        line_number = 1
        for line in lines:
            if not line.startswith(f"{line_number}. "):
                is_ordered_list = False
                break
            line_number += 1
        if is_ordered_list:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


        

    

    

        

