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
        if self.text == other.text:
            if self.text_type == other.text_type:
                if self.url == other.url:
                    return True
                return False
            return False
        return False
        
    def __repr__(self):
        #self alone may need to be adjusted - string format needed TextNode(TEXT, TEXT_TYPE, URL)
        return f"{self}({self.text}, {self.text_type}, {self.url})"
