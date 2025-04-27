
from enum import Enum
from functions import extract_markdown_images, extract_markdown_links

class TextType(Enum):
    TEXT = "t"
    BOLD = "b"
    ITALIC = "i"
    CODE = "code"
    LINK = "a"
    IMAGE = "img"

def text_node_to_html_node(text_node):
    from htmlnode import LeafNode
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Format not supported.")

#ch3 l1       
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    #old notes = list of TextNodes, text_type is enum
    new_nodes = []
    for node in old_nodes:
        if delimiter not in node.text:
            new_nodes.append(node)
            continue
            #raise Exception("Delimiter does is not in the Node")
        spl = node.text.split(delimiter)
        if (len(spl) - 1) % 2 != 0:
            raise Exception("Not enough splits")
        for i in range(0, len(spl)):
            if len(spl[i]) == 0:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(spl[i], node.text_type, node.url))
            else:
                new_nodes.append(TextNode(spl[i], text_type, node.url))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        ext = extract_markdown_images(node.text)
        if not ext:
            new_nodes.append(node)
            continue
            #if ext is nothing, old node is added to new_nodes
        text = node.text
        for img, link in ext:
            spl = text.split(f"![{img}]({link})", 1)
            if spl[0]:
                new_nodes.append(TextNode(spl[0], node.text_type, node.url))
            new_nodes.append(TextNode(img, TextType.IMAGE, link))
            #sets text to last string to perform additional splits 
            text = spl[-1]
        #once this loop ends, create the last object with remaining str - text
        if text:
            new_nodes.append(TextNode(text, node.text_type, node.url))
    return new_nodes
            

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        ext = extract_markdown_links(node.text)
        if not ext:
            new_nodes.append(node)
            continue
        
        text = node.text
        for link_text, link_url in ext:
            spl = text.split(f"[{link_text}]({link_url})", 1)
            if spl[0]:
                new_nodes.append(TextNode(spl[0], node.text_type, node.url))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            text = spl[-1]
            
        if text:
            new_nodes.append(TextNode(text, node.text_type, node.url))
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = [node]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
