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

    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props: list = None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have value")
        if self.props is not None and self.tag is None:
            raise ValueError("LeafNode with props requires a tag.")
        if self.props is None:
            if self.tag is None:
                return f"{self.value}"
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag=}, {self.value=}, {self.props=})"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict = None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node needs a tag.")
        if self.children is None:
            raise ValueError("Parent node requires children")
        if self.props is not None:
            parent_node_html = f"<{self.tag}{self.props_to_html()}>"
        else:
            parent_node_html = f"<{self.tag}>"
        for child_node in self.children:
            parent_node_html += child_node.to_html()
        parent_node_html += f"</{self.tag}>"
        return parent_node_html

    def __repr__(self):
        return f"ParentNode({self.tag=}, {self.children=}, {self.props=})"
