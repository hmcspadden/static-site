import unittest
from generate_page import *

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        md = """
# This is the title

And here is the body paragraph
"""
        title = extract_title(md)
        self.assertEqual(title, "This is the title")

        md = """
This is some markdown
without a **title**
"""
        with self.assertRaises(Exception):
            extract_title(md)

    

if __name__ == "__main__":
    unittest.main()