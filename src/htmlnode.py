class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if not self.tag:
            raise ValueError("HTMLNode must have a tag")

        if not self.children:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"

        children_html = "".join([child.to_html() for child in self.children])

        return f"<{self.tag} {self.props_to_html()}>{children_html}</{self.tag}>"

    def props_to_html(self):
        if not self.props:
            return ""

        return " ".join([f'{key}="{value}"' for key, value in self.props.items()])

    def __repr__(self):
        return f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"
