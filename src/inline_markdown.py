import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_image,
    text_type_link
)

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
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

def split_nodes_image(old_nodes):
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
    return re.findall(r"!\[([^\]]+)\]\(([^)]+)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", text)

def extract_title(markdown):
    title = re.search(r"^#\s+(.+)$", markdown, re.MULTILINE)

    if not title:
        raise ValueError("Title not found")

    return title.group(1)
