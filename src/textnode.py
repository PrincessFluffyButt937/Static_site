from enum import Enum

class TextType(Enum):
    BOLD = "b"
    ITALIC = "i"
    CODE = "c"
    LINK = "l"
    IMAGE = "I"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

        
    def __repr__(self):
        #self alone may need to be adjusted - string format needed TextNode(TEXT, TEXT_TYPE, URL)
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
