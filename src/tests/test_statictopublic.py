import unittest
from static_to_public import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = """# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.
"""
        header = extract_title(md)
        self.assertEqual(header, "Tolkien Fan Club")

    def test_extract_title_larger_header(self):
        md = """### Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.
"""
        with self.assertRaisesRegex(Exception, "Markdown file must start with an h1 header"):
            extract_title(md)

    def test_extract_title_indented_header(self):
        md = """    ### Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.
"""
        with self.assertRaisesRegex(Exception, "Markdown file must start with an h1 header"):
            extract_title(md)

    def test_extract_title_not_a_header(self):
        md = """```Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.
```
"""
        with self.assertRaisesRegex(Exception, "Markdown file must start with an h1 header"):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()