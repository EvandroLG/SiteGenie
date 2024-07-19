from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    """
    ParentNode represents an HTML element that can have child elements.
    It extends the HTMLNode class to create an HTML element with optional attributes and children.

    Attributes:
        children (list): A list of child HTMLNode objects.
        tag (str): The tag name of the HTML element (e.g., 'div', 'ul').
        props (dict, optional): A dictionary of HTML attributes and their values. Defaults to None.
    """

    def __init__(self, tag, children, props=None):
        """
        Initializes a ParentNode instance with the given children, tag, and properties.

        Args:
            children (list): A list of child HTMLNode objects.
            tag (str, optional): The tag name of the HTML element. Defaults to None.
            props (dict, optional): A dictionary of HTML attributes. Defaults to None.
        """

        super().__init__(tag, None, children, props)

    def to_html(self):
        """
        Converts the ParentNode to an HTML string representation.

        Returns:
            str: The HTML string representation of the ParentNode.

        Raises:
            ValueError: If the ParentNode does not have a tag.
            ValueError: If the ParentNode does not have children.
        """

        if not self.tag:
            raise ValueError("ParentNode must have a tag")

        if not self.children:
            raise ValueError("ParentNode must have children")

        children_html = "".join([child.to_html() for child in self.children])

        return f"<{self.tag} {self.props_to_html()}>{children_html}</{self.tag}>"
