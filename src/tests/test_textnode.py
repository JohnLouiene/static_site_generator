import unittest
from src.textnode import TextNode, TextType, text_node_to_html_node
from src.htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.BOLD, None)

        self.assertEqual(node, node2)
        self.assertEqual(node, node3)
        self.assertIsInstance(node, TextNode)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        node3 = TextNode("This is a text node with a different wording", TextType.TEXT)
        node4 = TextNode("This is a text node", TextType.BOLD, "testnonexistence.com")
        node5 = TextNode("This is a text node", TextType.BOLD, "testnotequal.com")

        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node4, node5)
        self.assertNotEqual(node, "Not a text node")

    def test_repr(self):
        TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
        self.assertIsNotNone(TextNode)

    def test_text(self):
        #text
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        #bold
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

        #italic
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")

        #code
        node = TextNode("print(This is a code node)", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print(This is a code node)")

        #link
        node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

        #image
        node = TextNode("alternate image", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "https://www.google.com", "alt": "alternate image"})

        #No Match
        node = TextNode("This is a text node", TextType.TEXT)
        node.text_type = "NONEXISTENT"
        with self.assertRaisesRegex(ValueError, "Unsupported text type: NONEXISTENT"):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()