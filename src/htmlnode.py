

from functions import markdown_to_blocks
from block import BlockType, block_to_block_type
from textnode import *

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("HTML node does not have to_html method")
    
    def props_to_html(self):
        if isinstance(self.props, dict):
            return "".join([f' {key}="{value}"' for key, value in self.props.items()if isinstance(key, str) and isinstance(value, str)])
        return ""
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode cannot have value = None")
        if self.tag == None:
            return self.value
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("In PattentNode, Tag cannot be None.")
        if self.children == None:
            raise ValueError("Children is None.")
        else:
            html = f"<{self.tag}{self.props_to_html()}>"

            for child in self.children:
                html += child.to_html()
        
            html += f"</{self.tag}>"

            return html

def text_to_children(text):
    text = text.replace("\n", " ")
    t_nodes = text_to_textnodes(text)
    l_nodes = []
    for t_node in t_nodes:
        l_nodes.append(text_node_to_html_node(t_node))
    return l_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match(block_type):
            case BlockType.PARAGRAPH:
                l_nodes = text_to_children(block)
                nodes.append(ParentNode("p", l_nodes))
            case BlockType.HEADING:
                heading = heading_converter(block)
                l_nodes = text_to_children(heading[1])
                nodes.append(ParentNode(f"h{heading[0]}", l_nodes))
            case BlockType.QUOTE:
                l_nodes = text_to_children(quote_converter(block))
                nodes.append(ParentNode("blockquote", l_nodes))
            case BlockType.CODE:
            # Only strip the triple backticks but preserve all whitespace, including trailing newlines
                block = block.strip("```").lstrip()
                # You might need to ensure there's exactly one trailing newline
                if not block.endswith("\n"):
                    block += "\n"
                child = [text_node_to_html_node(TextNode(block, TextType.TEXT))]
                code_node = [ParentNode("code", child)]
                pre_node = ParentNode("pre", code_node)
                nodes.append(pre_node)
            case BlockType.UNORDERED_LIST:
                li_nodes = li_nodes_wrapper(block)
                nodes.append(ParentNode("ul", li_nodes))
            case BlockType.ORDERED_LIST:
                li_nodes = li_nodes_wrapper(block)
                nodes.append(ParentNode("ol", li_nodes))
            case _:
                raise Exception("Unknown BlockType Enum")
    return ParentNode("div", nodes)

#helper for markdown_to_html_node()
def heading_converter(block):
    index = 0
    without_markdown = block
    for i in block:
        if i == "#":
            index += 1
            without_markdown = without_markdown[1:]
            continue
        break
    #index for h# format, other string striped of markdown formatting
    return index, without_markdown.lstrip()

def quote_converter(block):
    return "\n".join([line.lstrip(">").strip() for line in block.split("\n")])

def li_nodes_wrapper(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        new_line = line.split(" ", maxsplit=1)
        nodes = text_to_children(new_line[1])
        li_nodes.append(ParentNode("li", nodes))
    return li_nodes

