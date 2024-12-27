from static_site_gen.htmlnode import HTMLNode


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
    expected = f"HTMLNode(self.tag={tag}, self.value={value}, self.children=None, self.props={props})"
    html_props = node.props_to_html()
    assert html_props == ' href="google.com" target="__blank"'


def test_htmlnode_repr():
    tag = "a"
    value = "This is a test link"
    props = {"href": "google.com"}
    node = HTMLNode(tag=tag, value=value, props=props)
    expected = f"HTMLNode(self.tag='{tag}', self.value='{value}', self.children=None, self.props={props})"
    assert node.__repr__() == expected
