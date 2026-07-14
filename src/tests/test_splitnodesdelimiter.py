import unittest
from src.textnode import TextNode, TextType
from src.splitnodesdelimiter import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node_code = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes_code = split_nodes_delimiter([node_code], "`", TextType.CODE)

        node_bold = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes_bold = split_nodes_delimiter([node_bold], "**", TextType.BOLD)

        node_italic = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes_italic = split_nodes_delimiter([node_italic], "_", TextType.ITALIC)

        result_to_compare_code = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ]

        result_to_compare_bold = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        result_to_compare_italic = [
        TextNode("This is ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(new_nodes_code, result_to_compare_code)
        self.assertEqual(new_nodes_bold, result_to_compare_bold)
        self.assertEqual(new_nodes_italic, result_to_compare_italic)

    def test_split_nodes_delimiter_errors(self):
        node_with_no_closing_delimiter_code = TextNode("This has an opening `code span but no close", TextType.TEXT)
        node_with_no_closing_delimiter_bold = TextNode("This has **bold text but no closing marker", TextType.TEXT)
        node_with_no_closing_delimiter_italic = TextNode("This has _italic text but no closing marker", TextType.TEXT)

        node_not_a_text_type = TextNode("This has `code-looking text` but is already bold", TextType.BOLD)
        new_nodes_not_a_text_type = split_nodes_delimiter([node_not_a_text_type], "**", TextType.BOLD)

        with self.assertRaisesRegex(ValueError, "Invalid markdown syntax, missing closing delimiter"):
            split_nodes_delimiter([node_with_no_closing_delimiter_code], "`", TextType.CODE)
        with self.assertRaisesRegex(ValueError, "Invalid markdown syntax, missing closing delimiter"):
            split_nodes_delimiter([node_with_no_closing_delimiter_bold], "**", TextType.BOLD)
        with self.assertRaisesRegex(ValueError, "Invalid markdown syntax, missing closing delimiter"):
            split_nodes_delimiter([node_with_no_closing_delimiter_italic], "_", TextType.ITALIC)

        self.assertEqual(new_nodes_not_a_text_type, [node_not_a_text_type])
        
if __name__ == "__main__":
    unittest.main()