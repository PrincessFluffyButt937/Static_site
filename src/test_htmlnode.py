import unittest

from htmlnode import *

class TestTextNode(unittest.TestCase):

# html node tests

    def test_prompt1(self):
        node1 = HTMLNode("p", "hello world", ["hi", "susan"], {"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("p", "hello world", ["hi", "susan"], {"href": "https://www.google.com", "target": "_blank"})
        node3 = HTMLNode("p", "hello world", ["hi", "susan"], {"href": "https://www.google.com", "target": "_blank"})
        p1, p2, p3 = node1.props_to_html(), node2.props_to_html(), node3.props_to_html()
        self.assertEqual(p1, p2, p3)

    def test_promp2(self):
        node1 = HTMLNode("p", "hello world", ["hi", "susan", None])
        node2 = HTMLNode("p", "hello world", ["hi", "susan"])
        node3 = HTMLNode("p", "hello world", ["hi", "susan"], "hello there")
        p1, p2, p3 = node1.props_to_html(), node2.props_to_html(), node3.props_to_html()
        self.assertEqual(p1, p2, p3)

    def test_promp3(self):
        node1 = HTMLNode("p", "hello world", ["hi", "susan", None])
        node2 = HTMLNode("p", "hello world", ["hi", "susan"], {"href": "https://www.google.com", "target": "_blank"})
        node3 = HTMLNode("p", "hello world", ["hi", "susan"])
        p1, p2, p3 = node1.props_to_html(), node2.props_to_html(), node3.props_to_html()
        self.assertNotEqual(p1, p2, p3)    

#leaf node tests

    def test_leaf_to_html_p1(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_p3(self):
        node = LeafNode(value="Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_p4(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

# parent node tests

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

    def test_to_html_with_grandchildren1(self):
        n1 = LeafNode("b", "Hello")
        n2 = LeafNode("I", "There")
        n3 = LeafNode(tag=None, value="no tag str")
        p1 = ParentNode("obi", [n1, n2])
        p2 = ParentNode("t", [n3])
        final = ParentNode("w", [p1, p2])
        self.assertEqual(
            final.to_html(),
            "<w><obi><b>Hello</b><I>There</I></obi><t>no tag str</t></w>"
        )

    def test_to_html_with_grandchildren2(self):
        n1 = LeafNode("b", "Hello", {})
        n2 = LeafNode("I", "There", {"general": "Kenobi"})
        n3 = LeafNode(tag=None, value="no tag str")
        p1 = ParentNode("obi", [n1, n2])
        p2 = ParentNode("t", [n3])
        final = ParentNode("w", [p1, p2], {"Darth": "Vader"})
        self.assertEqual(
            final.to_html(),
            '<w Darth="Vader"><obi><b>Hello</b><I general="Kenobi">There</I></obi><t>no tag str</t></w>'
        )

    def test_to_html_with_grandchildren3(self):
        n1 = LeafNode("b", None, {})
        n2 = LeafNode("I", "There", {"general": "Kenobi"})
        n3 = LeafNode(tag=None, value="no tag str")
        p1 = ParentNode("obi", [n1, n2])
        p2 = ParentNode("t", [n3])
        final = ParentNode("w", [p1, p2], {"Darth": "Vader"})
        self.assertRaises(ValueError, msg="LeafNode cannot have value = None")