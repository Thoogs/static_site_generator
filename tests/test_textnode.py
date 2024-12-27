from static_site_gen.textnode import TextNode, TextType


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
