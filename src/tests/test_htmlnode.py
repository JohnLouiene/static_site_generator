import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode

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
    
class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_mixed_grandchildren(self):
        grandchild_node_1 = LeafNode("b", "first_grandchild")
        grandchild_node_2 = LeafNode(None, "second_grandchild")
        grandchild_node_3 = LeafNode("b", "third_grandchild")
        grandchild_node_4 = LeafNode(None, "fourth_grandchild")
        grandchild_parent_node_1 = ParentNode("p", [grandchild_node_2, grandchild_node_3, grandchild_node_4])
        grandchild_parent_node_2 = ParentNode("span", [grandchild_parent_node_1])
        child_node = ParentNode("span", [grandchild_node_1, grandchild_parent_node_2])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>first_grandchild</b><span><p>second_grandchild<b>third_grandchild</b>fourth_grandchild</p></span></span></div>",
        )

    def test_to_html_props(self):
        child_node_with_props = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        parent_node_with_props = ParentNode("div", [child_node_with_props], {"class": "container", "id": "main"})

        child_node_without_props = LeafNode("a", "Click me!")
        parent_node_without_props = ParentNode("div", [child_node_without_props])

        self.assertEqual(parent_node_with_props.to_html(), f'<div class="container" id="main"><a href="https://www.google.com">Click me!</a></div>')
        self.assertEqual(parent_node_without_props.to_html(), f'<div><a>Click me!</a></div>')

    def test_to_html_parent_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaisesRegex(ValueError, "Parent node is missing a tag parameter"):
            parent_node.to_html()

    def test_to_html_parent_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaisesRegex(ValueError, "Parent node is missing child nodes in children list"):
            parent_node.to_html()

    def test_to_html_parent_empty_children_list(self):
        parent_node = ParentNode("div", [])
        with self.assertRaisesRegex(ValueError, "Parent node is missing child nodes in children list"):
            parent_node.to_html()