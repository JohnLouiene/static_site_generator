import unittest
from src.textblocks import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            blocks
        )

    def test_markdown_to_blocks_empty(self):
        md = """
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [],
            blocks
        )

    def test_markdown_to_blocks_whole_block(self):
        md = """
This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "This is **bolded** paragraph"
                "\nThis is another paragraph with _italic_ text and `code` here"
                "\nThis is the same paragraph on a new line"
                "\n- This is a list"
                "\n- with items",
            ],
            blocks
        )

    def test_markdown_to_blocks_extra_indent(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            blocks
        )

    def test_markdown_to_blocks_extra_indent(self):
        md = """
****

``

-
-
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "****",
                "``",
                "-\n-",
            ],
            blocks
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        result = block_to_block_type("A paragraph")
        self.assertEqual(result, BlockType.PARAGRAPH)

        result = block_to_block_type("### A heading")
        self.assertEqual(result, BlockType.HEADING)

        result = block_to_block_type("```\n A code line```")
        self.assertEqual(result, BlockType.CODE)

        result = block_to_block_type("```\n Still ``` a code line```")
        self.assertEqual(result, BlockType.CODE)

        result = block_to_block_type("> A quote\n> of quotes")
        self.assertEqual(result, BlockType.QUOTE)

        result = block_to_block_type("> A quote\n>of quotes")
        self.assertEqual(result, BlockType.QUOTE)

        result = block_to_block_type("- An unordered list\n- of paragraphs")
        self.assertEqual(result, BlockType.UNORDERED_LIST)

        result = block_to_block_type("1. An ordered list\n2. of paragraphs")
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_block_to_block_type_malformed_to_paragraphs(self):
        result = block_to_block_type("###Not a heading")
        self.assertEqual(result, BlockType.PARAGRAPH)

        result = block_to_block_type(" ###Not a heading")
        self.assertEqual(result, BlockType.PARAGRAPH)

        result = block_to_block_type("###")
        self.assertEqual(result, BlockType.PARAGRAPH)

        result = block_to_block_type("###                     ")
        self.assertEqual(result, BlockType.PARAGRAPH)

        result = block_to_block_type("```Not a code line```")
        self.assertEqual(result, BlockType.PARAGRAPH)

        result = block_to_block_type("> Not a quote\n but a paragraph")
        self.assertEqual(result, BlockType.PARAGRAPH)

        result = block_to_block_type("- Not an unordered list\nJust paragraphs")
        self.assertEqual(result, BlockType.PARAGRAPH)

        result = block_to_block_type("- Not an unordered list\n-Just paragraphs")
        self.assertEqual(result, BlockType.PARAGRAPH)

        result = block_to_block_type("1. Not an ordered list\nJust paragraphs")
        self.assertEqual(result, BlockType.PARAGRAPH)

        result = block_to_block_type("2. Not an ordered list\n1. Just paragraphs")
        self.assertEqual(result, BlockType.PARAGRAPH)

        result = block_to_block_type("1. Not an ordered list\n3. Just paragraphs")
        self.assertEqual(result, BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()

