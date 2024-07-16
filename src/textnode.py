from leafnode import LeafNode


text_type_text = "text"
text_type_link = "link"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_image = "image"


class TextNode:
    """
    TextNode represents a piece of text with an associated type and optional URL.
    It can be converted into an HTML representation using LeafNode.

    Attributes:
        text (str): The text content.
        text_type (str): The type of the text
        url (str, optional): The URL associated with the text. Defaults to None.
    """

    def __init__(self, text, text_type, url=None):
        """
        Initializes a TextNode instance with the given text, text type, and optional URL.

        Args:
            text (str): The text content.
            text_type (str): The type of the text.
            url (str, optional): The URL associated with the text. Defaults to None.
        """

        self.text = text
        self.text_type = text_type
        self.url = url

    def to_html_node(self):
        """
        Converts the TextNode to a LeafNode, representing the HTML element.

        Returns:
            LeafNode: The LeafNode instance representing the HTML element.

        Raises:
            ValueError: If the text_type is invalid.
        """

        if self.text_type == text_type_text:
            return LeafNode(None, self.text)
        if self.text_type == text_type_link:
            return LeafNode("a", self.text, {"href": self.url})
        if self.text_type == text_type_bold:
            return LeafNode("b", self.text)
        if self.text_type == text_type_italic:
            return LeafNode("i", self.text)
        if self.text_type == text_type_code:
            return LeafNode("code", self.text)
        if self.text_type == text_type_image:
            return LeafNode("img", None, {"src": self.url, "alt": self.text})

        raise ValueError(f"Invalid text type: {self.text_type}")

    def __eq__(self, other):
        """
        Checks the equality of two TextNode instances.

        Args:
            other (TextNode): The other TextNode instance to compare.

        Returns:
            bool: True if both TextNode instances are equal, False otherwise.
        """

        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        """
        Returns a string representation of the TextNode instance for debugging.

        Returns:
            str: The string representation of the TextNode.
        """

        return f"Text: {self.text}, Type: {self.text_type}, URL: {self.url}"
