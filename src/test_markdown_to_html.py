from markdown_to_html import *
import unittest

class TestMarkdownHTML(unittest.TestCase):

    def test_text_to_children(self):
        md = "This is another **paragraph** with _italic_ text and `code` here"
        children = text_to_children(md)
        self.assertEqual(
            [
                LeafNode(None, "This is another "),
                LeafNode("b", "paragraph"),
                LeafNode(None, " with "),
                LeafNode("i", "italic"),
                LeafNode(None, " text and "),
                LeafNode("code", "code"),
                LeafNode(None, " here")
            ], 
            children
        )
        md = "An ![image](https://picsum.photos/) and a [link](https://google.com/)"
        children = text_to_children(md)
        self.assertEqual(
            [
                LeafNode(None, "An "),
                LeafNode("img", "", {"src" : "https://picsum.photos/", "alt" : "image"}),
                LeafNode(None, " and a "),
                LeafNode("a", "link", {"href" : "https://google.com/"})
            ],
            children
        )

    def test_heading(self):
        md = "#### This is a lvl 4 heading"
        h4 = heading_to_html(md)
        self.assertEqual(
            ParentNode("h4", [LeafNode(None, "This is a lvl 4 heading")]),
            h4
        )
        md = "## This is a **lvl 2** heading with _emphasis_"
        h2 = heading_to_html(md)
        self.assertEqual(
            ParentNode(
                "h2",
                [
                    LeafNode(None, "This is a "),
                    LeafNode("b", "lvl 2"),
                    LeafNode(None, " heading with "),
                    LeafNode("i", "emphasis")
                ]
            ),
            h2
        )
    
    def test_quote(self):
        md = ">First _line_ in a quote\n>Second **line** in a quote\n>Final `line` in a quote"
        quote = quote_to_html(md)
        self.assertEqual(
            ParentNode(
                "blockquote",
                [
                    LeafNode(None, "First "),
                    LeafNode("i", "line"),
                    LeafNode(None, " in a quote<br />Second "),
                    LeafNode("b", "line"),
                    LeafNode(None, " in a quote<br />Final "),
                    LeafNode("code", "line"),
                    LeafNode(None, " in a quote")
                ]
            ),
            quote
        )

    def test_unordered(self):
        md = "- **item** in list\n- another _item_\n- final item"
        unordered = unordered_to_html(md)
        self.assertEqual(
            ParentNode(
                "ul",
                [
                    ParentNode("li", [
                        LeafNode("b", "item"),
                        LeafNode(None, " in list")
                    ]),
                    ParentNode("li", [
                        LeafNode(None, "another "),
                        LeafNode("i", "item")
                    ]),
                    ParentNode("li", [
                        LeafNode(None, "final item")
                    ])
                ]
            ),
            unordered
        )

    def test_ordered(self):
        md = "1. **item** in list\n2. another _item_\n3. final item"
        ordered = ordered_to_html(md)
        self.assertEqual(
            ParentNode(
                "ol",
                [
                    ParentNode("li", [
                        LeafNode("b", "item"),
                        LeafNode(None, " in list")
                    ]),
                    ParentNode("li", [
                        LeafNode(None, "another "),
                        LeafNode("i", "item")
                    ]),
                    ParentNode("li", [
                        LeafNode(None, "final item")
                    ])
                ]
            ),
            ordered
        )

    def test_code(self):
        md = "```This is text that _should_ remain the **same** even with inline stuff```"
        code = code_to_html(md)
        self.assertEqual(
            ParentNode("pre", [
                LeafNode("code", "This is text that _should_ remain the **same** even with inline stuff")
            ]),
            code
        )

    def test_paragraph(self):
        md = "This is just a **regular** paragraph block"
        paragraph = paragraph_to_html(md)
        self.assertEqual(
            ParentNode("p", [
                LeafNode(None, "This is just a "),
                LeafNode("b", "regular"),
                LeafNode(None, " paragraph block")
            ]),
            paragraph
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
            "<div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_md_to_html(self):
        self.maxDiff = None
        md = """
### This is a **header**

> This is a _quote_
> between two lines

- an item
- another item

1. first ![image](https://picsum.photos/)
2. second [link](https://google.com/)

This is the rest of the paragraph
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            ("<div><h3>This is a <b>header</b></h3><blockquote> This is a <i>quote</i><br /> between two lines</blockquote><ul><li>an item</li><li>another item</li></ul><ol><li>first <img src=\"https://picsum.photos/\" alt=\"image\"></img></li><li>second <a href=\"https://google.com/\">link</a></li></ol><p>This is the rest of the paragraph</p></div>")
        )

if __name__ == "__main__":
    unittest.main()