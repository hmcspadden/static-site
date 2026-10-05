import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="p", value="hello", props={"href" : "google.com"})
        node2 = HTMLNode(tag="p", value="hello", props={"href" : "google.com"})
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode(tag="p", value="hello", props={"href" : "google.com"})
        self.assertEqual(node.props_to_html(), " href=\"google.com\"")
        node2 = HTMLNode(tag="p", value="hello", props={"href" : "google.com", "target" : "_blank"})
        self.assertEqual(node2.props_to_html(), " href=\"google.com\" target=\"_blank\"")

    def test_leafnode_to_html(self):
        node = LeafNode(tag="p", value="hello", props={"href" : "google.com"})
        self.assertEqual(node.to_html(), "<p href=\"google.com\">hello</p>")
        node2 = LeafNode(tag=None, value="hello", props={"href" : "google.com"})
        self.assertEqual(node2.to_html(), "hello")
        
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
    
    def test_parent_edge(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text")
            ]
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

if __name__ == "__main__":
    unittest.main()