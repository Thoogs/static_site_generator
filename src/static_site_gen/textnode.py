from enum import Enum

class TextType(Enum):
    MD_TEXT = "text"
    MD_BOLD = "bold"
    MD_ITALIC = "italic"
    MD_CODE = "code"
    MD_LINK = "link"
    MD_IMAGE = "image"

class TextNode():
    def __init__(self, text: str, text_type: str, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
