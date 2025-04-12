import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq1(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        self.assertNotEqual(node, node2)
    
    def test_eq2(self):
        node = TextNode("This is a text not a node", TextType.BOLD)
        node2 = TextNode("", TextType.BOLD, "www.google.com")
        self.assertNotEqual(node, node2)

    def test_eq3(self):
        node = TextNode(None, TextType.BOLD)
        node2 = TextNode("This is a text not a node", TextType.BOLD, "www.google.com")
        self.assertNotEqual(node, node2)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text1(self):
        node = TextNode("This is a text node", "ass")
        with self.assertRaises(Exception, msg="Format not supported."):
            text_node_to_html_node(node)

    def test_text2(self):
        node = TextNode("This is a text node", TextType.LINK, "test.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.to_html(), '<a href="test.com">This is a text node</a>')

if __name__ == "__main__":
    unittest.main()