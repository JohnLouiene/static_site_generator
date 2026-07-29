import unittest
from block_to_html import markdown_to_html_node

class TestBlockToHTML(unittest.TestCase):
    def test_unordered_list_block(self):
        md = """
- Line 1 with **bolded** paragraph
- Line 2 with _italic_ text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Line 1 with <b>bolded</b> paragraph</li><li>Line 2 with <i>italic</i> text</li></ul></div>",
        ) 

    def test_ordered_list_block(self):
            md = """
1. Line 1 with **bolded** paragraph
2. Line 2 with _italic_ text
"""
    
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><ol><li>Line 1 with <b>bolded</b> paragraph</li><li>Line 2 with <i>italic</i> text</li></ol></div>",
            ) 

    def test_heading_block(self):
            md = """
### This is a heading
"""
    
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><h3>This is a heading</h3></div>",
            ) 

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_ul_malformed_to_paragraphs(self):
        md = """
- Line 1 with **bolded** paragraph
- Line 2 with _italic_ text
turned into a paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>- Line 1 with <b>bolded</b> paragraph - Line 2 with <i>italic</i> text turned into a paragraph</p></div>",
        ) 

    def test_ol_malformed_to_paragraphs(self):
        md = """
1. Line 1 with **bolded** paragraph
2. Line 2 with _italic_ text
turned into a paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>1. Line 1 with <b>bolded</b> paragraph 2. Line 2 with <i>italic</i> text turned into a paragraph</p></div>",
        )

    def test_code_malformed_to_paragraphs(self):
        md = """
``
This is text that _should not_ remain
the **same** even with inline stuff
with some `code`
``
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p> This is text that <i>should not</i> remain the <b>same</b> even with inline stuff with some <code>code</code> </p></div>",
        )

if __name__ == "__main__":
    unittest.main()