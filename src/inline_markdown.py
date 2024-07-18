import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_image,
    text_type_link,
    text_type_bold,
    text_type_italic,
    text_type_code,
)


def text_to_textnodes(text):
    """
    Converts a text string into a list of TextNode objects, splitting the text into nodes for text, images, and links.

    Args:
        text (str): The input text string.

    Returns:
        list: A list of TextNode objects.
    """

    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits TextNode objects by a specified delimiter.

    Args:
        old_nodes (list): A list of TextNode objects.
        delimiter (str): The delimiter to split the text on.
        text_type (str): The text type to assign to the split segments.

    Returns:
        list: A list of TextNode objects after splitting by the delimiter.

    Raises:
        ValueError: If the delimiter usage is invalid in the text.
    """

    new_nodes = []

    for node in old_nodes:
        if node.text_type == text_type_text:
            if not _is_valid_delimiter(node.text, delimiter):
                raise ValueError("Invalid markdown")

            fragments = node.text.split(delimiter)

            for i, fragment in enumerate(fragments):
                if i % 2 == 0:
                    new_nodes.append(TextNode(fragment, text_type_text))
                else:
                    new_nodes.append(TextNode(fragment, text_type))
        else:
            new_nodes.append(node)

    return new_nodes


def _is_valid_delimiter(text, delimiter):
    """
    Checks if the delimiter usage is valid in the text.

    Args:
        text (str): The input text string.
        delimiter (str): The delimiter to check.

    Returns:
        bool: True if the delimiter count is even, False otherwise.
    """

    return text.count(delimiter) % 2 == 0


def split_nodes_image(old_nodes):
    """
    Splits TextNode objects containing image markdown into separate objects for text and images.

    Args:
        old_nodes (list): A list of TextNode objects.

    Returns:
        list: A list of TextNode objects after splitting images.
    """

    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        original_text = node.text
        images = extract_markdown_images(node.text)

        if not images:
            new_nodes.append(node)
            continue

        pos = 0
        for alt_text, url in images:
            start = original_text.find(f"![{alt_text}]({url})", pos)
            if start == -1:
                raise ValueError("Invalid markdown")

            if pos < start:
                new_nodes.append(TextNode(original_text[pos:start], text_type_text))

            new_nodes.append(TextNode(alt_text, text_type_image, url))

            pos = start + len(f"![{alt_text}]({url})")

        if pos < len(original_text):
            new_nodes.append(TextNode(original_text[pos:], text_type_text))

    return new_nodes


def split_nodes_link(old_nodes):
    """
    Splits TextNode objects containing link markdown into separate objects for text and links.

    Args:
        old_nodes (list): A list of TextNode objects.

    Returns:
        list: A list of TextNode objects after splitting links.
    """

    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        original_text = node.text
        links = extract_markdown_links(node.text)

        if not links:
            new_nodes.append(node)
            continue

        pos = 0
        for link_text, url in links:
            start = original_text.find(f"[{link_text}]({url})", pos)
            if start == -1:
                raise ValueError("Invalid markdown")

            if pos < start:
                new_nodes.append(TextNode(original_text[pos:start], text_type_text))

            new_nodes.append(TextNode(link_text, text_type_link, url))

            pos = start + len(f"[{link_text}]({url})")

        if pos < len(original_text):
            new_nodes.append(TextNode(original_text[pos:], text_type_text))

    return new_nodes


def extract_markdown_images(text):
    """
    Extracts image markdown from a text string.

    Args:
        text (str): The input text string.

    Returns:
        list: A list of tuples, each containing the alt text and URL of an image.
    """

    return re.findall(r"!\[([^\]]+)\]\(([^)]+)\)", text)


def extract_markdown_links(text):
    """
    Extracts link markdown from a text string.

    Args:
        text (str): The input text string.

    Returns:
        list: A list of tuples, each containing the link text and URL of a link.
    """

    return re.findall(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", text)


def extract_title(markdown):
    """
    Extracts the title from a markdown string.

    Args:
        markdown (str): The input markdown string.

    Returns:
        str: The title extracted from the markdown.

    Raises:
        ValueError: If a title is not found in the markdown.
    """

    title = re.search(r"^#\s+(.+)$", markdown, re.MULTILINE)

    if not title:
        raise ValueError("Title not found")

    return title.group(1)
