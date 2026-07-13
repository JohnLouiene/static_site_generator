import unittest
from src.htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_isInstance(self):
        paragraph = HTMLNode("p", "This is a paragraph")
        link = HTMLNode("a", "this is a link", props={ "href": "https://www.google.com", "target": "_blank"})
        list_item_1 = HTMLNode("li", "Apples")
        list_item_2 = HTMLNode("li", "Bananas")
        unordered_list = HTMLNode("ul", children=[list_item_1, list_item_2])

        self.assertIsInstance(paragraph, HTMLNode)
        self.assertIsInstance(link, HTMLNode)
        self.assertIsInstance(list_item_1, HTMLNode)
        self.assertIsInstance(unordered_list, HTMLNode)

    def test_to_html(self):
        pass

    def test_props_to_html(self):
        node = HTMLNode("a", "this is a link", props={ "href": "https://www.google.com", "target": "_blank"})

        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_repr(self):
        node = HTMLNode("a", "this is a link", props={ "href": "https://www.google.com", "target": "_blank"})

        self.assertEqual(repr(node), "tag:a, value:this is a link, children:None, props:{'href': 'https://www.google.com', 'target': '_blank'}")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This text has no tag.")
        self.assertEqual(node.to_html(), "This text has no tag.")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "This is a short paragraph.")
        self.assertEqual(node.to_html(), "<p>This is a short paragraph.</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_repr(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(repr(node), "tag:a, value:Click me!, props:{'href': 'https://www.google.com'}")