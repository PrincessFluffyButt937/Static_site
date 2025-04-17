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

    def test_delimiter1(self):
        node = TextNode('Hi, split this **bold** text please', TextType.TEXT)
        out = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(f'{out}', '[TextNode(Hi, split this , TextType.TEXT, None), TextNode(bold, TextType.BOLD, None), TextNode( text please, TextType.TEXT, None)]')

    #def test_delimiter2(self):
        #node = TextNode('Hi, split this **bold** text please', TextType.TEXT)
        #with self.assertRaises(Exception, msg="Delimiter does is not in the Node"):
        #    split_nodes_delimiter([node], "__", TextType.BOLD)
    
    def test_delimiter3(self):
        node = TextNode('Hi, split this **bold** text** please', TextType.TEXT)
        with self.assertRaises(Exception, msg="Not enough splits"):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_delimiter4(self):
        node = TextNode('Hi, split this **bold text please', TextType.TEXT)
        with self.assertRaises(Exception, msg="Not enough splits"):
            split_nodes_delimiter([node], "**", TextType.BOLD)
        
    def test_delimiter5(self):
        node = TextNode('**Hi**, split this bold text please', TextType.TEXT)
        out = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(f'{out}', '[TextNode(Hi, TextType.BOLD, None), TextNode(, split this bold text please, TextType.TEXT, None)]')
    
    def test_delimiter5(self):
        node = TextNode('**Hi**, split this bold text please', TextType.TEXT)
        node1 = TextNode('Hi, split this **bold** text please', TextType.TEXT)
        out = split_nodes_delimiter([node, node1], "**", TextType.BOLD)
        self.assertEqual(f'{out}', '[TextNode(Hi, TextType.BOLD, None), TextNode(, split this bold text please, TextType.TEXT, None), TextNode(Hi, split this , TextType.TEXT, None), TextNode(bold, TextType.BOLD, None), TextNode( text please, TextType.TEXT, None)]')
    
    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            new_nodes,
        )

    def test_split_link1(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev) hello", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" hello", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_link2(self):
        node = TextNode("[to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev) hello", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" hello", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        out = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            out
        )


if __name__ == "__main__":
    unittest.main()