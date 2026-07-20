def markdown_to_blocks(markdown: str):
    blocks = markdown.split("\n\n")
    result = []

    for block in blocks:
        stripped_block = block.strip()
        
        if stripped_block != '':
            result.append(stripped_block)

    return result

