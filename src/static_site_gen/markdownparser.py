import re
from enum import Enum

from static_site_gen.htmlnode import ParentNode
from static_site_gen.textnode import TextNode, TextType, text_node_to_html_node


class MarkdownBlockType(Enum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    CODE = "code"
    QUOTE = "quote"
    UO_LIST = "unordered list"
    O_LIST = "ordered list"


def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType) -> list:
    new_nodes = []
    for node in old_nodes:
        # We only want to edit text nodes, so others get immediately added as is
        if node.text_type != TextType.MD_TEXT:
            new_nodes.append(node)
            continue
        sections = node.text.split(delimiter)
        # Delimiter needs to have matching pair to be valid markdown
        if len(sections) % 2 == 0:
            raise SyntaxError("Invalid markdown syntax")
        # each section needs to be converted to node
        for idx in range(len(sections)):
            if idx % 2 == 1:
                new_nodes.append(TextNode(sections[idx], text_type))
            else:
                # Make sure the section is more than empty string
                if len(sections[idx]) != 0:
                    new_nodes.append(TextNode(sections[idx], TextType.MD_TEXT))
    return new_nodes


def extract_markdown_images(text: str) -> list:
    markdown_images_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    images = re.findall(markdown_images_pattern, text)
    return images


def extract_markdown_links(text: str) -> list:
    markdown_links_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    links = re.findall(markdown_links_pattern, text)
    return links


def split_nodes_images(old_nodes: list) -> list:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.MD_TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        # If we have no images, just add it and skip to next node
        if len(images) == 0:
            new_nodes.append(node)
            continue
        node_text = node.text
        # If we do have images, go through all of them and create new nodes
        for image in images:
            node_text = split_element(node_text, image, new_nodes, TextType.MD_IMAGE)
        if len(node_text) > 0:
            new_nodes.append(TextNode(node_text, TextType.MD_TEXT))
    return new_nodes


def split_nodes_links(old_nodes: list) -> list:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.MD_TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        # If we have no links, just add the node and skip to next node
        if len(links) == 0:
            new_nodes.append(node)
            continue
        node_text = node.text
        # If we do have links, go through all of them and create new nodes
        for link in links:
            node_text = split_element(node_text, link, new_nodes, TextType.MD_LINK)
        if len(node_text) > 0:
            new_nodes.append(TextNode(node_text, TextType.MD_TEXT))
    return new_nodes


def split_element(text: str, element: tuple, nodes: list, element_type: TextType):
    if element_type == TextType.MD_LINK:
        sections = text.split(f"[{element[0]}]({element[1]})", maxsplit=1)
    if element_type == TextType.MD_IMAGE:
        sections = text.split(f"![{element[0]}]({element[1]})", maxsplit=1)
    if len(sections) != 2:
        raise SyntaxError("Invalid markdown, element not properly closed")
    text = sections[1]
    # Add the text before the element if any..
    if len(sections[0]) > 0:
        nodes.append(TextNode(sections[0], TextType.MD_TEXT))
    # Then add the element node itself
    nodes.append(TextNode(element[0], element_type, element[1]))
    return text


def text_to_textnodes(inline_markdown: str) -> list:
    origin_node = TextNode(inline_markdown, TextType.MD_TEXT)
    textnodes = [origin_node]
    textnodes = split_nodes_links(textnodes)
    textnodes = split_nodes_images(textnodes)
    textnodes = split_nodes_delimiter(textnodes, "**", TextType.MD_BOLD)
    textnodes = split_nodes_delimiter(textnodes, "_", TextType.MD_ITALIC)
    textnodes = split_nodes_delimiter(textnodes, "`", TextType.MD_CODE)
    return textnodes


def markdown_to_blocks(markdown_document: str) -> list:
    raw_blocks = markdown_document.split("\n\n")
    cleaned_blocks = []
    for block in raw_blocks:
        block = block.strip()
        if len(block) == 0:
            continue
        cleaned_blocks.append(block)
    return cleaned_blocks


def block_to_block_type(markdown_block: str) -> MarkdownBlockType:
    block_type = MarkdownBlockType.PARAGRAPH
    if is_heading(markdown_block):
        block_type = MarkdownBlockType.HEADING
    elif is_code(markdown_block):
        block_type = MarkdownBlockType.CODE
    elif is_quote(markdown_block):
        block_type = MarkdownBlockType.QUOTE
    elif is_unordered_list(markdown_block):
        block_type = MarkdownBlockType.UO_LIST
    elif is_ordered_list(markdown_block):
        block_type = MarkdownBlockType.O_LIST
    return block_type


def is_heading(markdown_block: str) -> bool:
    heading_pattern = r"^#{1,6}\ \w"
    if re.search(heading_pattern, markdown_block) is None:
        return False
    return True


def is_code(markdown_block: str) -> bool:
    return markdown_block.startswith("```") and markdown_block.endswith("```")


def is_quote(markdown_block: str) -> bool:
    for line in markdown_block.split("\n"):
        if not line.startswith(">"):
            return False
    return True


def is_unordered_list(markdown_block: str) -> bool:
    for line in markdown_block.split("\n"):
        if not line.startswith("- ") and not line.startswith("* "):
            return False
    return True


def is_ordered_list(markdown_block: str) -> bool:
    markdown_lines = markdown_block.split("\n")
    for idx in range(len(markdown_lines)):
        if not markdown_lines[idx].startswith(f"{idx + 1}. "):
            return False
    return True


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def convert_block_to_paragraph(markdown_block: str) -> ParentNode:
    node_children = text_to_children(markdown_block)
    paragraph_node = ParentNode("p", children=node_children)
    return paragraph_node


def convert_block_to_heading(markdown_block: str) -> ParentNode:
    # Count heading level and strip markdown characters
    heading_level = markdown_block.count("#", 0, 5)
    markdown_block = markdown_block.lstrip("# ")

    node_children = text_to_children(markdown_block)
    heading_node = ParentNode(f"h{heading_level}", children=node_children)
    return heading_node


def convert_block_to_code(markdown_block: str) -> ParentNode:
    # Strip markdown code block characters
    markdown_block = markdown_block.strip("`")

    node_children = text_to_children(markdown_block)
    code_node = ParentNode("pre", children=[])
    code_node.children.append(ParentNode("code", children=node_children))
    return code_node


def convert_block_to_quote(markdown_block: str) -> ParentNode:
    # Strip markdown quote block characters
    markdown_lines = markdown_block.split("\n")
    markdown_block_cleaned = ""
    for idx in range(0, len(markdown_lines)):
        markdown_lines[idx] = markdown_lines[idx].lstrip("> ")
        markdown_block_cleaned += markdown_lines[idx] + "\n"

    node_children = text_to_children(markdown_block_cleaned.strip())
    quote_node = ParentNode("blockquote", children=node_children)
    return quote_node


def convert_block_to_list(markdown_block: str, ordered: bool = False) -> ParentNode:
    # Strip markdown list characters
    markdown_lines = markdown_block.split("\n")
    markdown_block_cleaned = ""
    for idx in range(0, len(markdown_lines)):
        if not ordered:
            markdown_lines[idx] = markdown_lines[idx].lstrip("- ")
        if ordered:
            markdown_lines[idx] = markdown_lines[idx].lstrip(f"{idx + 1}. ")
        markdown_block_cleaned += markdown_lines[idx] + "\n"

    items = markdown_block_cleaned.strip().split("\n")
    html_items = []
    for item in items:
        children = text_to_children(item)
        html_items.append(ParentNode("li", children))

    # Create appropriate parent node
    if ordered:
        list_node = ParentNode("ol", children=html_items)
    if not ordered:
        list_node = ParentNode("ul", children=html_items)
    return list_node


def markdown_to_html_node(markdown: str) -> ParentNode:
    document_node = ParentNode("div", children=[])
    markdown_blocks = markdown_to_blocks(markdown)
    for markdown_block in markdown_blocks:
        block_type = block_to_block_type(markdown_block)
        match block_type:
            case MarkdownBlockType.PARAGRAPH:
                document_node.children.append(
                    convert_block_to_paragraph(markdown_block)
                )
            case MarkdownBlockType.HEADING:
                document_node.children.append(convert_block_to_heading(markdown_block))
            case MarkdownBlockType.CODE:
                document_node.children.append(convert_block_to_code(markdown_block))
            case MarkdownBlockType.QUOTE:
                document_node.children.append(convert_block_to_quote(markdown_block))
            case MarkdownBlockType.UO_LIST:
                document_node.children.append(convert_block_to_list(markdown_block))
            case MarkdownBlockType.O_LIST:
                document_node.children.append(
                    convert_block_to_list(markdown_block, ordered=True)
                )
    return document_node


def extract_title(markdown: str) -> str:
    markdown = markdown.strip()
    markdown_lines = markdown.split("\n")
    heading_pattern = r"^#\s+(.*)$"
    for line in markdown_lines:
        heading = re.findall(heading_pattern, line)
        if len(heading) != 0:
            break
    if len(heading) == 0:
        raise Exception("Document is missing h1 header.")
    # extract the first heading 1 from document, we expect there are no more than 1
    heading = heading[0]
    heading = heading.lstrip("# ")
    heading = heading.strip()
    return heading
