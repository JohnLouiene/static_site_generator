import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.BOLD, None)

        self.assertEqual(node, node2)
        self.assertEqual(node2, node3)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.PLAIN)
        node3 = TextNode("This is a text node with a different wording", TextType.PLAIN)

        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)

    def test_repr(self):
        TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

        self.assertIsNotNone(TextNode)

if __name__ == "__main__":
    unittest.main()