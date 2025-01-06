import re

from static_site_gen.textnode import TextType, TextNode


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


def text_to_textnodes(text: str) -> list:
    origin_node = TextNode(text, TextType.MD_TEXT)
    textnodes = [origin_node]
    textnodes = split_nodes_links(textnodes)
    textnodes = split_nodes_images(textnodes)
    textnodes = split_nodes_delimiter(textnodes, "**", TextType.MD_BOLD)
    textnodes = split_nodes_delimiter(textnodes, "*", TextType.MD_ITALIC)
    textnodes = split_nodes_delimiter(textnodes, "`", TextType.MD_CODE)
    return textnodes
