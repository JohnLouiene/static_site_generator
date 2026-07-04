from textnode import TextType, TextNode

def main():
    TestExample = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(TestExample)

main()