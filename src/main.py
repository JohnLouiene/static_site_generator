from src.textnode import TextType, TextNode
from src.htmlnode import HTMLNode

def main():
    TestExample = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(TestExample)
    TestExample2 = HTMLNode("a", "this is a link", None, { "href": "https://www.google.com", "target": "_blank"})
    props_to_html_test = TestExample2.props_to_html()
    print(props_to_html_test)

main()