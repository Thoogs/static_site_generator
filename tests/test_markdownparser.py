import pytest

from static_site_gen.htmlnode import LeafNode, ParentNode
from static_site_gen.markdownparser import (
    MarkdownBlockType,
    block_to_block_type,
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    markdown_to_html_node,
    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_links,
    text_to_textnodes,
)
from static_site_gen.textnode import TextNode, TextType


def test_split_nodes_delimiter_bold():
    old_node = [
        TextNode(
            "This is text with a **bolded phrase** in the middle", TextType.MD_TEXT
        )
    ]
    delimiter = "**"
    expected = [
        TextNode("This is text with a ", TextType.MD_TEXT),
        TextNode("bolded phrase", TextType.MD_BOLD),
        TextNode(" in the middle", TextType.MD_TEXT),
    ]

    nodes = split_nodes_delimiter(old_node, delimiter, TextType.MD_BOLD)
    assert nodes == expected


def test_split_nodes_delimiter_code():
    old_node = [TextNode("This is text with a `code block`", TextType.MD_TEXT)]
    delimiter = "`"
    expected = [
        TextNode("This is text with a ", TextType.MD_TEXT),
        TextNode("code block", TextType.MD_CODE),
    ]

    nodes = split_nodes_delimiter(old_node, delimiter, TextType.MD_CODE)
    assert nodes == expected


def test_split_nodes_delimiter_bold_and_italic():
    old_node = [
        TextNode(
            "This is text with a **bolded phrase** in *the* middle", TextType.MD_TEXT
        )
    ]
    delimiter = "**"
    expected = [
        TextNode("This is text with a ", TextType.MD_TEXT),
        TextNode("bolded phrase", TextType.MD_BOLD),
        TextNode(" in ", TextType.MD_TEXT),
        TextNode("the", TextType.MD_ITALIC),
        TextNode(" middle", TextType.MD_TEXT),
    ]

    nodes = split_nodes_delimiter(old_node, delimiter, TextType.MD_BOLD)
    delimiter = "*"
    nodes = split_nodes_delimiter(nodes, delimiter, TextType.MD_ITALIC)
    assert nodes == expected


def test_split_nodes_delimiter_multiple_blocks():
    old_node = [
        TextNode(
            "This is text with a `code block`, more text with `code`", TextType.MD_TEXT
        )
    ]
    delimiter = "`"
    expected = [
        TextNode("This is text with a ", TextType.MD_TEXT),
        TextNode("code block", TextType.MD_CODE),
        TextNode(", more text with ", TextType.MD_TEXT),
        TextNode("code", TextType.MD_CODE),
    ]

    nodes = split_nodes_delimiter(old_node, delimiter, TextType.MD_CODE)
    assert nodes == expected


def test_split_nodes_delimiter_multiple_nodes():
    old_node = [
        TextNode(
            "This is text with a `code block`, more text with `code`", TextType.MD_TEXT
        ),
        TextNode("Another node with more `code`", TextType.MD_TEXT),
    ]
    delimiter = "`"
    expected = [
        TextNode("This is text with a ", TextType.MD_TEXT),
        TextNode("code block", TextType.MD_CODE),
        TextNode(", more text with ", TextType.MD_TEXT),
        TextNode("code", TextType.MD_CODE),
        TextNode("Another node with more ", TextType.MD_TEXT),
        TextNode("code", TextType.MD_CODE),
    ]

    nodes = split_nodes_delimiter(old_node, delimiter, TextType.MD_CODE)
    assert nodes == expected


def test_split_nodes_delimiter_non_text_node():
    old_node = [
        TextNode(
            "This is text with a `code block`, more text with `code`", TextType.MD_CODE
        )
    ]
    delimiter = "`"
    expected = [
        TextNode(
            "This is text with a `code block`, more text with `code`", TextType.MD_CODE
        )
    ]

    nodes = split_nodes_delimiter(old_node, delimiter, TextType.MD_CODE)
    assert nodes == expected


def test_split_nodes_delimiter_invalid_markdown():
    old_node = [TextNode("This is text with a `code block", TextType.MD_TEXT)]
    delimiter = "`"
    with pytest.raises(SyntaxError, match="Invalid markdown syntax"):
        split_nodes_delimiter(old_node, delimiter, TextType.MD_CODE)


def test_extract_markdown_image():
    text = "Here is an ![image of images](google.com)"
    images = extract_markdown_images(text)
    assert images == [("image of images", "google.com")]


def test_extract_markdown_image_multiple():
    text = "Here is an ![image of images](google.com) and there is also a ![rick roll](rickroll.com)"
    images = extract_markdown_images(text)
    assert images == [("image of images", "google.com"), ("rick roll", "rickroll.com")]


def test_extract_markdown_links():
    text = "Here is [google](google.com)"
    links = extract_markdown_links(text)
    assert links == [("google", "google.com")]


def test_extract_markdown_links_multiple():
    text = "Here is [google](google.com) and there is also [youtube](youtube.com)"
    links = extract_markdown_links(text)
    assert links == [("google", "google.com"), ("youtube", "youtube.com")]


def test_extract_markdown_links_and_images():
    text = (
        "Here is [google](google.com) and there is also ![youtube image](youtube.com)"
    )
    links = extract_markdown_links(text)
    images = extract_markdown_images(text)
    assert links == [("google", "google.com")]
    assert images == [("youtube image", "youtube.com")]


def test_split_nodes_links():
    node = [
        TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.MD_TEXT,
        )
    ]
    new_nodes = split_nodes_links(node)
    expected = [
        TextNode("This is text with a link ", TextType.MD_TEXT),
        TextNode("to boot dev", TextType.MD_LINK, "https://www.boot.dev"),
        TextNode(" and ", TextType.MD_TEXT),
        TextNode("to youtube", TextType.MD_LINK, "https://www.youtube.com/@bootdotdev"),
    ]
    assert new_nodes == expected


def test_split_nodes_images():
    nodes = [
        TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.MD_TEXT,
        )
    ]
    new_nodes = split_nodes_images(nodes)
    expected = [
        TextNode("This is text with an image ", TextType.MD_TEXT),
        TextNode("to boot dev", TextType.MD_IMAGE, "https://www.boot.dev"),
        TextNode(" and ", TextType.MD_TEXT),
        TextNode(
            "to youtube", TextType.MD_IMAGE, "https://www.youtube.com/@bootdotdev"
        ),
    ]
    assert new_nodes == expected


def test_split_nodes_images_and_links():
    nodes = [
        TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.MD_TEXT,
        )
    ]
    new_nodes = split_nodes_images(nodes)
    new_nodes = split_nodes_links(new_nodes)
    expected = [
        TextNode("This is text with an image ", TextType.MD_TEXT),
        TextNode("to boot dev", TextType.MD_IMAGE, "https://www.boot.dev"),
        TextNode(" and ", TextType.MD_TEXT),
        TextNode("to youtube", TextType.MD_LINK, "https://www.youtube.com/@bootdotdev"),
    ]
    assert new_nodes == expected


def test_split_nodes_single_image_node():
    nodes = [
        TextNode(
            "![to boot dev](https://www.boot.dev)",
            TextType.MD_TEXT,
        )
    ]
    new_nodes = split_nodes_images(nodes)
    expected = [
        TextNode("to boot dev", TextType.MD_IMAGE, "https://www.boot.dev"),
    ]
    assert new_nodes == expected


def test_text_to_textnode():
    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    new_nodes = text_to_textnodes(text)
    expected = [
        TextNode("This is ", TextType.MD_TEXT),
        TextNode("text", TextType.MD_BOLD),
        TextNode(" with an ", TextType.MD_TEXT),
        TextNode("italic", TextType.MD_ITALIC),
        TextNode(" word and a ", TextType.MD_TEXT),
        TextNode("code block", TextType.MD_CODE),
        TextNode(" and an ", TextType.MD_TEXT),
        TextNode(
            "obi wan image", TextType.MD_IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
        ),
        TextNode(" and a ", TextType.MD_TEXT),
        TextNode("link", TextType.MD_LINK, "https://boot.dev"),
    ]
    assert new_nodes == expected


def test_markdown_to_blocks():
    markdown_doc = "# heading\n\nParagraph text within the document\nThat can span multiple lines\n\n* list item 1\n* list item 2\n"
    expected = [
        "# heading",
        "Paragraph text within the document\nThat can span multiple lines",
        "* list item 1\n* list item 2",
    ]
    assert markdown_to_blocks(markdown_doc) == expected


def test_markdown_to_blocks_extra_newlines_and_space():
    markdown_doc = "# heading\n\n\n\n\n     Paragraph text within the document\nThat can span multiple lines                  \n\n* list item 1\n* list item 2\n"
    expected = [
        "# heading",
        "Paragraph text within the document\nThat can span multiple lines",
        "* list item 1\n* list item 2",
    ]
    assert markdown_to_blocks(markdown_doc) == expected


def test_markdown_to_blocks_multiline_str():
    markdown_doc = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
    expected = [
        "This is **bolded** paragraph",
        "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
        "* This is a list\n* with items",
    ]
    assert markdown_to_blocks(markdown_doc) == expected


def test_block_to_block_type():
    markdown_block = "# Heading"
    assert block_to_block_type(markdown_block.strip()) == MarkdownBlockType.HEADING
    markdown_block = "#### Heading"
    assert block_to_block_type(markdown_block.strip()) == MarkdownBlockType.HEADING


def test_block_to_block_type_code():
    markdown_block = """
```print('hello world')```
"""
    assert block_to_block_type(markdown_block.strip()) == MarkdownBlockType.CODE


def test_block_to_block_type_unordered_list():
    markdown_block = """
* This is a list
* with items
"""
    assert block_to_block_type(markdown_block.strip()) == MarkdownBlockType.UO_LIST


def test_block_to_block_type_ordered_list():
    markdown_block = """
1. This is a list
2. with items
"""
    assert block_to_block_type(markdown_block.strip()) == MarkdownBlockType.O_LIST


def test_block_to_block_type_quote():
    markdown_block = """
> This is a list
> with items
"""
    assert block_to_block_type(markdown_block.strip()) == MarkdownBlockType.QUOTE


def test_block_to_block_type_paragraph_dirty():
    markdown_block = """
This is a block with naughty syntax
# with items
"""
    assert block_to_block_type(markdown_block.strip()) == MarkdownBlockType.PARAGRAPH


def test_markdown_to_html_node():
    markdown_block = """
# This is a test doc

With simple paragraph block
"""
    expected = ParentNode("div", children=[])
    expected_child_1 = ParentNode(
        tag="h1", children=[LeafNode(None, "This is a test doc")]
    )
    expected_child_2 = ParentNode(
        tag="p", children=[LeafNode(None, "With simple paragraph block")]
    )
    expected.children.append(expected_child_1)
    expected.children.append(expected_child_2)
    assert markdown_to_html_node(markdown_block) == expected


def test_markdown_to_html_node_with_many_blocks():
    markdown_block = """
# This is a test doc

With simple paragraph block

* lists are also cool
* with multiple items

1. sometimes they need order
2. and continue too

```print("hello parser")```

> Sometimes code be, sometimes not
> it can also **be bold** or *leaning*
"""
    expected = ParentNode("div", children=[])
    header_child = ParentNode(tag="h1", children=[LeafNode(None, "This is a test doc")])
    paragraph_child = ParentNode(
        tag="p", children=[LeafNode(None, "With simple paragraph block")]
    )
    unordered_child = ParentNode(
        tag="ul",
        children=[
            ParentNode("li", [LeafNode(tag=None, value="lists are also cool")]),
            ParentNode("li", [LeafNode(tag=None, value="with multiple items")]),
        ],
    )
    ordered_child = ParentNode(
        tag="ol",
        children=[
            ParentNode("li", [LeafNode(tag=None, value="sometimes they need order")]),
            ParentNode("li", [LeafNode(tag=None, value="and continue too")]),
        ],
    )
    code_child = ParentNode(
        tag="code", children=[LeafNode(None, 'print("hello parser")')]
    )
    quote_child = ParentNode(
        tag="blockquote",
        children=[
            LeafNode(None, "Sometimes code be, sometimes not\nit can also "),
            LeafNode("b", "be bold"),
            LeafNode(None, " or "),
            LeafNode("i", "leaning"),
        ],
    )
    expected.children.append(header_child)
    expected.children.append(paragraph_child)
    expected.children.append(unordered_child)
    expected.children.append(ordered_child)
    expected.children.append(code_child)
    expected.children.append(quote_child)

    assert markdown_to_html_node(markdown_block) == expected


def test_markdown_to_html_code():
    markdown_block = """
# This is a test doc

With simple paragraph block

* lists are also cool
* with multiple items

1. sometimes they need order
2. and continue too

```print("hello parser")```

> Sometimes code be, sometimes not
> it can also **be bold** or *leaning*
"""
    expected = '<div><h1>This is a test doc</h1><p>With simple paragraph block</p><ul><li>lists are also cool</li><li>with multiple items</li></ul><ol><li>sometimes they need order</li><li>and continue too</li></ol><code>print("hello parser")</code><blockquote>Sometimes code be, sometimes not\nit can also <b>be bold</b> or <i>leaning</i></blockquote></div>'

    assert markdown_to_html_node(markdown_block).to_html() == expected
