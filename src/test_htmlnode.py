import unittest

from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):
    def test_prompt1(self):
        node1 = HTMLNode("p", "hello world", ["hi", "susan"], {"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("p", "hello world", ["hi", "susan"], {"href": "https://www.google.com", "target": "_blank"})
        node3 = HTMLNode("p", "hello world", ["hi", "susan"], {"href": "https://www.google.com", "target": "_blank"})
        p1, p2, p3 = node1.props_to_html(), node2.props_to_html(), node3.props_to_html()
        print(f"p1={p1}")
        self.assertEqual(p1, p2, p3)

    def test_promp2(self):
        node1 = HTMLNode("p", "hello world", ["hi", "susan", None])
        node2 = HTMLNode("p", "hello world", ["hi", "susan"])
        node3 = HTMLNode("p", "hello world", ["hi", "susan"], "hello there")
        p1, p2, p3 = node1.props_to_html(), node2.props_to_html(), node3.props_to_html()
        print(f"p1={p1}")
        print(f"p3={p3}")
        self.assertEqual(p1, p2, p3)

    def test_promp3(self):
        node1 = HTMLNode("p", "hello world", ["hi", "susan", None])
        node2 = HTMLNode("p", "hello world", ["hi", "susan"], {"href": "https://www.google.com", "target": "_blank"})
        node3 = HTMLNode("p", "hello world", ["hi", "susan"])
        p1, p2, p3 = node1.props_to_html(), node2.props_to_html(), node3.props_to_html()
        self.assertNotEqual(p1, p2, p3)    
