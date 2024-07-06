import re

from textnode import (
    TextNode,
    text_type_text,
)

def split_node_delimiter(old_nodes, delimiter, text_type):
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

    return new_nodes

def _is_valid_delimiter(text, delimiter):
    return text.count(delimiter) % 2 == 0

def extract_markdown_images(text):
    return re.findall(r"!\[([^\]]+)\]\(([^)]+)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", text)

