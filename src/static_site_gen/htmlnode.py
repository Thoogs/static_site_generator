class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list = None,
        props: dict = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return None
        props_html = ""
        for prop, value in self.props.items():
            props_html += f' {prop}="{value}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag=}, {self.value=}, {self.children=}, {self.props=})"
