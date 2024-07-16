from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    """
    LeafNode represents an HTML element that does not have any child elements.
    It extends the HTMLNode class to create a single HTML element with optional attributes and value.

    Attributes:
        tag (str): The tag name of the HTML element (e.g., 'div', 'span').
        value (str): The inner text or HTML of the element.
        props (dict): A dictionary of HTML attributes and their values.
    """

    def __init__(self, tag=None, value=None, props=None):
        """
        Initializes a LeafNode instance with the given tag, value, and properties.

        Args:
            tag (str, optional): The tag name of the HTML element. Defaults to None.
            value (str, optional): The inner text or HTML of the element. Defaults to None.
            props (dict, optional): A dictionary of HTML attributes. Defaults to None.
        """

        super().__init__(tag, value, None, props)

    def to_html(self):
        """
        Converts the LeafNode to an HTML string representation.

        Returns:
            str: The HTML string representation of the LeafNode.
        """

        props_html = f" {self.props_to_html()}" if self.props else ""
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
