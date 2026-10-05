import unittest
from block_converter import *

class TestBlockConverter(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_block_heading(self):
        md = "### This is a heading"
        self.assertEqual(BlockType.HEADING, block_to_block_type(md))
    
    def test_block_code(self):
        md = "``` This is a code block ```"
        self.assertEqual(BlockType.CODE, block_to_block_type(md))
    
    def test_block_quote(self):
        md = ">this is one quote line\n> this is another\n> and finally a third"
        self.assertEqual(BlockType.QUOTE, block_to_block_type(md))

    def test_block_unordered(self):
        md = "- an item in a list\n- another item\n- final item in list"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(md))

    def test_block_ordered(self):
        md = "1. This is the first item\n2. This is the second item\n3. This is the third item"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(md))

    def test_block_paragraph(self):
        md = "This is just a plain paragraph"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))

if __name__ == "__main__":
    unittest.main()