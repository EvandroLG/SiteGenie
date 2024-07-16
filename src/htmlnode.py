class HTMLNode:
    """
    HTMLNode represents an HTML element, which can have a tag, value, children, and properties.

    Attributes:
        tag (str): The tag name of the HTML element (e.g., 'div', 'span').
        value (str): The inner text or HTML of the element.
        children (list): A list of child HTMLNode objects.
        props (dict): A dictionary of HTML attributes and their values.
    """

    def __init__(self, tag=None, value=None, children=None, props=None):
        """
        Initializes an HTMLNode instance with the given tag, value, children, and properties.

        Args:
            tag (str, optional): The tag name of the HTML element. Defaults to None.
            value (str, optional): The inner text or HTML of the element. Defaults to None.
            children (list, optional): A list of child HTMLNode objects. Defaults to None.
            props (dict, optional): A dictionary of HTML attributes. Defaults to None.
        """

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """
        Converts the HTMLNode to an HTML string representation.

        Returns:
            str: The HTML string representation of the HTMLNode.

        Raises:
            ValueError: If the HTMLNode does not have a tag.
        """

        if not self.tag:
            raise ValueError("HTMLNode must have a tag")

        if not self.children:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"

        children_html = "".join([child.to_html() for child in self.children])

        return f"<{self.tag} {self.props_to_html()}>{children_html}</{self.tag}>"

    def props_to_html(self):
        """
        Converts the properties dictionary to an HTML attribute string.

        Returns:
            str: The HTML attribute string representation of the properties.
        """

        if not self.props:
            return ""

        return " ".join([f'{key}="{value}"' for key, value in self.props.items()])

    def __repr__(self):
        """
        Returns a string representation of the HTMLNode instance for debugging.

        Returns:
            str: The string representation of the HTMLNode.
        """

        return f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"
