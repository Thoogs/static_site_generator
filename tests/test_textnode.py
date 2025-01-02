import pytest

from static_site_gen.textnode import TextNode, TextType, text_node_to_html_node


def test_eq():
    node = TextNode("This is a test node", TextType.MD_BOLD)
    node2 = TextNode("This is a test node", TextType.MD_BOLD)
    assert node == node2


def test_eq_url():
    node = TextNode("This is a test node", TextType.MD_BOLD, "www.google.com")
    node2 = TextNode("This is a test node", TextType.MD_BOLD, "www.google.com")
    assert node == node2


def test_not_eq():
    node = TextNode("This is a test node", TextType.MD_BOLD)
    node2 = TextNode("This is a test node", TextType.MD_BOLD, "www.google.com")
    assert node != node2


def test_not_eq_texttype():
    node = TextNode("This is a test node", TextType.MD_BOLD)
    node2 = TextNode("This is a test node", TextType.MD_ITALIC)
    assert node != node2


def test_not_eq_text():
    node = TextNode("This is a test node", TextType.MD_BOLD)
    node2 = TextNode("This is a test node but with more", TextType.MD_BOLD)
    assert node != node2


def test_textnode_to_leafnode():
    node = TextNode("This is a test node", TextType.MD_BOLD)
    html_node = text_node_to_html_node(node)
    assert html_node.value == "This is a test node"
    assert html_node.tag == "b"
    assert html_node.props is None


def test_textnode_to_leafnode_with_props():
    node = TextNode("This is a test node", TextType.MD_LINK, "google.com")
    html_node = text_node_to_html_node(node)
    assert html_node.value == "This is a test node"
    assert html_node.tag == "a"
    assert html_node.props == {"href": "google.com"}


def test_textnode_to_leafnode_without_tag():
    node = TextNode("This is a test node", TextType.MD_TEXT)
    html_node = text_node_to_html_node(node)
    assert html_node.value == "This is a test node"
    assert html_node.tag is None
    assert html_node.props is None


def test_textnode_to_leafnode_image():
    node = TextNode("This is a test image", TextType.MD_IMAGE, "https://www.boot.dev")
    html_node = text_node_to_html_node(node)
    assert html_node.value == ""
    assert html_node.tag == "img"
    assert html_node.props == {
        "alt": "This is a test image",
        "src": "https://www.boot.dev",
    }


def test_textnode_to_leafnode_unsupported_type():
    node = TextNode("This is a text", "gibberish", "google.com")
    with pytest.raises(ValueError, match="Unsupported textnode type."):
        text_node_to_html_node(node)
