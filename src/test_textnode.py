import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is the first node", TextType.ITALIC)
        node2 = TextNode("This is the second node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        node3 = TextNode("This is a node", TextType.ITALIC)
        node4 = TextNode("This is a node", TextType.TEXT)
        self.assertNotEqual(node3, node4)
        node5 = TextNode("This is a node", TextType.LINK, "reddit.com")
        node6 = TextNode("This is a node", TextType.LINK, "google.com")
        self.assertNotEqual(node5, node6)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        node2 = TextNode("image", TextType.IMAGE, "https://picsum.photos/")
        html_node2 = text_node_to_html_node(node2)
        self.assertEqual(html_node2.props, {"src" : "https://picsum.photos/", "alt" : "image"})

if __name__ == "__main__":
    unittest.main()