import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()