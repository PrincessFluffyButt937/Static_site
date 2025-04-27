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

    def test_leaf_to_html_p1(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_p3(self):
        node = LeafNode(value="Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_p4(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

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
    
    #helper functions tests

    def test_quote_format0(self):
        block = ">Hello there.\n>I am your death.\n>Prepare yourself."
        result = quote_converter(block)
        self.assertEqual(result, "Hello there.\nI am your death.\nPrepare yourself.")
    
    def test_heading_counter(self):
        block = "### "
        result = heading_converter(block)
        self.assertEqual(result[0], 3)
        self.assertEqual(result[1], "")
    
    def test_heading_counter1(self):
        block = "###### this should be simple"
        result = heading_converter(block)
        self.assertEqual(result[0], 6)
        self.assertEqual(result[1], "this should be simple")
    
    def test_heading_counter2(self):
        block = "# #"
        result = heading_converter(block)
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], "#")
    
    def test_heading_counter3(self):
        block = "#### hi there"
        result = heading_converter(block)
        self.assertEqual(result[0], 4)
        self.assertEqual(result[1], "hi there")
    

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
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
    ### This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is <b>bolded</b> paragraph text in a p tag here</h3><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_ol(self):
        md = """
    1. This is **bolded** paragraph
    2. text in a p
    3. tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is <b>bolded</b> paragraph</li><li>text in a p</li><li>tag here</li></ol><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_ul(self):
        md = """
    - This is **bolded** paragraph
    - text in a p
    - tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is <b>bolded</b> paragraph</li><li>text in a p</li><li>tag here</li></ul><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_quote(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    >This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><blockquote>This is another paragraph with <i>italic</i> text and <code>code</code> here</blockquote></div>",
        )