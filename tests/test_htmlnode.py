from static_site_gen.htmlnode import HTMLNode, LeafNode
import pytest


def test_htmlnode_without_props():
    node = HTMLNode(tag="p", value="This is a test paragraph")
    html_props = node.props_to_html()
    assert html_props is None


def test_htmlnode_with_props():
    node = HTMLNode(tag="a", value="This is a test link", props={"href": "google.com"})
    html_props = node.props_to_html()
    assert html_props == ' href="google.com"'


def test_htmlnode_multiple_props():
    tag = "a"
    value = "This is a test link"
    props = {"href": "google.com", "target": "__blank"}
    node = HTMLNode(tag=tag, value=value, props=props)
    html_props = node.props_to_html()
    assert html_props == ' href="google.com" target="__blank"'


def test_htmlnode_repr():
    tag = "a"
    value = "This is a test link"
    props = {"href": "google.com"}
    node = HTMLNode(tag=tag, value=value, props=props)
    expected = f"HTMLNode(self.tag='{tag}', self.value='{value}', self.children=None, self.props={props})"
    assert node.__repr__() == expected


def test_leafnode_no_tag_no_prop():
    value = "This is a test link"
    node = LeafNode(tag=None, value=value)
    node_html = node.to_html()
    expected = "This is a test link"
    assert node_html == expected


def test_leafnode_tag_no_prop():
    tag = "p"
    value = "This is a test paragraph"
    node = LeafNode(tag=tag, value=value)
    node_html = node.to_html()
    expected = "<p>This is a test paragraph</p>"
    assert node_html == expected


def test_leafnode_tag_prop():
    tag = "a"
    value = "This is a test link"
    props = {"href": "google.com", "target": "__blank"}
    node = LeafNode(tag=tag, value=value, props=props)
    node_html = node.to_html()
    expected = '<a href="google.com" target="__blank">This is a test link</a>'
    assert node_html == expected


def test_leafnode_props_without_tag():
    value = "This is a test link"
    props = {"href": "google.com", "target": "__blank"}
    node = LeafNode(tag=None, value=value, props=props)
    with pytest.raises(ValueError, match="LeafNode with props requires a tag."):
        node.to_html()
