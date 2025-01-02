from enum import Enum
from static_site_gen.htmlnode import LeafNode


class TextType(Enum):
    MD_TEXT = "text"
    MD_BOLD = "bold"
    MD_ITALIC = "italic"
    MD_CODE = "code"
    MD_LINK = "link"
    MD_IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: str, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(textnode):
    match textnode.text_type:
        case TextType.MD_TEXT:
            return LeafNode(tag=None, value=textnode.text)
        case TextType.MD_BOLD:
            return LeafNode(tag="b", value=textnode.text)
        case TextType.MD_ITALIC:
            return LeafNode(tag="i", value=textnode.text)
        case TextType.MD_CODE:
            return LeafNode(tag="code", value=textnode.text)
        case TextType.MD_IMAGE:
            return LeafNode(
                tag="img", value="", props={"src": textnode.url, "alt": textnode.text}
            )
        case TextType.MD_LINK:
            return LeafNode(tag="a", value=textnode.text, props={"href": textnode.url})
        case _:
            raise ValueError("Unsupported textnode type.")
