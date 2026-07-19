import unittest
from src.textnode import TextNode, TextType
from src.md_parsing_functions import split_nodes_delimiter, split_nodes_image, split_nodes_link, extract_markdown_images, extract_markdown_links

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node_code = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes_code = split_nodes_delimiter([node_code], "`", TextType.CODE)
        result_to_compare_code = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ]
        self.assertEqual(new_nodes_code, result_to_compare_code)

        node_bold = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes_bold = split_nodes_delimiter([node_bold], "**", TextType.BOLD)
        result_to_compare_bold = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes_bold, result_to_compare_bold)

        node_italic = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes_italic = split_nodes_delimiter([node_italic], "_", TextType.ITALIC)
        result_to_compare_italic = [
        TextNode("This is ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes_italic, result_to_compare_italic)

    def test_split_nodes_delimiter_errors(self):
        node_with_no_closing_delimiter_code = TextNode("This has an opening `code span but no close", TextType.TEXT)
        with self.assertRaisesRegex(ValueError, "Invalid markdown syntax, missing closing delimiter"):
            split_nodes_delimiter([node_with_no_closing_delimiter_code], "`", TextType.CODE)

        node_with_no_closing_delimiter_bold = TextNode("This has **bold text but no closing marker", TextType.TEXT)
        with self.assertRaisesRegex(ValueError, "Invalid markdown syntax, missing closing delimiter"):
            split_nodes_delimiter([node_with_no_closing_delimiter_bold], "**", TextType.BOLD)
        
        node_with_no_closing_delimiter_italic = TextNode("This has _italic text but no closing marker", TextType.TEXT)
        with self.assertRaisesRegex(ValueError, "Invalid markdown syntax, missing closing delimiter"):
            split_nodes_delimiter([node_with_no_closing_delimiter_italic], "_", TextType.ITALIC)

        node_not_a_text_type = TextNode("This has `code-looking text` but is already bold", TextType.BOLD)
        new_nodes_not_a_text_type = split_nodes_delimiter([node_not_a_text_type], "**", TextType.BOLD)
        self.assertEqual(new_nodes_not_a_text_type, [node_not_a_text_type])

class TestExtractImageFromMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_images_no_match(self):
        matches = extract_markdown_images("This is text with no matches")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_no_match(self):
        matches = extract_markdown_images("This is text with ![]()")
        self.assertListEqual([("","")], matches)

        matches_alt_text = extract_markdown_images("This is text with ![image]()")
        self.assertListEqual([("image","")], matches_alt_text)

        matches_anchor_text = extract_markdown_images("This is text with ![](https://i.imgur.com/aKaOqIh.gif)")
        self.assertListEqual([("","https://i.imgur.com/aKaOqIh.gif")], matches_anchor_text)

    def test_extract_markdown_images_not_links(self):
        matches = extract_markdown_images( "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([], matches)

class TestExtractLinkFromMarkdown(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links_no_match(self):
        matches = extract_markdown_images( "This is text with a link []()")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_no_text_in_bracket(self):
        matches = extract_markdown_links("This is text with []()")
        self.assertListEqual([("","")], matches)

        matches_alt_text = extract_markdown_links("This is text with [link]()")
        self.assertListEqual([("link","")], matches_alt_text)

        matches_anchor_text = extract_markdown_links("This is text with [](https://www.boot.dev)")
        self.assertListEqual([("","https://www.boot.dev")], matches_anchor_text)

    def test_extract_markdown_links_not_images(self):
        matches = extract_markdown_images( "This is text with an image [image](https://i.imgur.com/aKaOqIh.gif)")
        self.assertListEqual([], matches)

class TestSplitNodesImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) one",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" one", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_split_images_empty(self):
        node = TextNode(
            "This is text with an ![]()",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("", TextType.IMAGE, ""),
            ],
            new_nodes,
        )
    
    def test_split_images_no_images(self):
        node = TextNode(
            "This is text with only a string",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with only a string", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_images_beginning(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) this is text with a string at the end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" this is text with a string at the end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_end(self):
        node = TextNode(
            "This is text with a string at the end ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with a string at the end ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_multiple_images(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![image](https://i.imgur.com/zjjcJKZ.png)![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_empty(self):
        node = TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")

        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],
            new_nodes,
        )    

    def test_split_images_malformed(self):
        node = TextNode(
            "[image](https://i.imgur.com/zjjcJKZ.png this is text with a string at the end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("[image](https://i.imgur.com/zjjcJKZ.png this is text with a string at the end", TextType.TEXT),
            ],
            new_nodes,
        )

class TestSplitNodesLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](boot.dev) and another [second link](youtube.com) one",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "youtube.com"),
                TextNode(" one", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_links_empty(self):
        node = TextNode(
            "This is text with an ![]()",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("", TextType.LINK, ""),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode(
            "This is text with only a string",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with only a string", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_beginning(self):
        node = TextNode(
            "[link](boot.dev) this is text with a string at the end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "boot.dev"),
                TextNode(" this is text with a string at the end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_end(self):
        node = TextNode(
            "This is text with a string at the end [link](boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a string at the end ", TextType.TEXT),
                TextNode("link", TextType.LINK, "boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links_multiple_links(self):
        node = TextNode(
            "[link](boot.dev)[link](boot.dev)[link](boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "boot.dev"),
                TextNode("link", TextType.LINK, "boot.dev"),
                TextNode("link", TextType.LINK, "boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links_empty(self):
        node = TextNode("link", TextType.LINK, "boot.dev")

        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("link", TextType.LINK, "boot.dev")],
            new_nodes,
        )

    def test_split_links_malformed(self):
        node = TextNode(
            "[link](boot.dev this is text with a string at the end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("[link](boot.dev this is text with a string at the end", TextType.TEXT),
            ],
            new_nodes,
        )
    
if __name__ == "__main__":
    unittest.main()