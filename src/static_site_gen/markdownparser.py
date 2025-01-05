from static_site_gen.textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType) -> list:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.MD_TEXT:
            new_nodes.append(node)
            continue
        split_node = node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise SyntaxError("Invalid markdown syntax")
        for idx in range(len(split_node)):
            if idx % 2 == 1:
                new_nodes.append(TextNode(split_node[idx], text_type))
            else:
                if len(split_node[idx]) != 0:
                    new_nodes.append(TextNode(split_node[idx], TextType.MD_TEXT))
    return new_nodes
