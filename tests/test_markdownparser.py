import pytest
from static_site_gen.markdownparser import split_nodes_delimiter
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
