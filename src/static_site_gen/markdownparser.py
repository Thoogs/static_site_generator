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
