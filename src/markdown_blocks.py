import re

from inline_markdown import text_to_textnodes
from parentnode import ParentNode

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quota = "quota"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_block(markdown):
    """
    Splits a markdown string into individual blocks based on newlines.

    Args:
        markdown (str): The input markdown string.

    Returns:
        list: A list of blocks (strings) from the markdown.
    """

    fragments = markdown.split("\n")
    blocks = []

    for fragment in fragments:
        if fragment == "":
            continue

        blocks.append(fragment.strip())

    return blocks


def block_to_block_type(block):
    """
    Determines the type of a block of text based on its content.

    Args:
        block (str): The block of text.

    Returns:
        str: The type of the block.
    """

    if re.match(r"^\s*#{1,6}\s", block):
        return block_type_heading

    if block.startswith("```") and block.endswith("```"):
        return block_type_code

    if block.startswith(">"):
        return block_type_quota

    if re.match(r"^[*-]\s", block):
        return block_type_unordered_list

    if re.match(r"^\d+\.\s", block):
        return block_type_ordered_list

    return block_type_paragraph


def markdown_to_html_node(markdown):
    """
    Converts markdown text to a hierarchical structure of HTML nodes.

    Args:
        markdown (str): The markdown text to be converted.

    Returns:
        ParentNode: The root node containing the HTML structure.
    """

    blocks = markdown_to_block(markdown)
    i = 0
    children = []

    while i < len(blocks):
        block = blocks[i]
        block_type = block_to_block_type(block)

        if block_type == block_type_paragraph:
            children.append(paragraph_to_html_node(block))
        elif block_type == block_type_heading:
            children.append(heading_to_html_node(block))
        elif block_type == block_type_code:
            children.append(code_to_html_node(block))
        elif block_type == block_type_quota:
            children.append(quote_to_html_node(block))
        elif block_type == block_type_unordered_list:
            i, ul = ul_to_html_node(i, blocks)
            children.append(ul)
        elif block_type == block_type_ordered_list:
            i, ol = ol_to_html_node(i, blocks)
            children.append(ol)

        i += 1

    return ParentNode("div", children)


def text_to_children(text):
    """
    Converts plain text into a list of HTML text node children.

    Args:
        text (str): The text to be converted.

    Returns:
        list: A list of HTML nodes representing the text.
    """

    text_nodes = text_to_textnodes(text)
    children = []

    for text_node in text_nodes:
        children.append(text_node.to_html_node())

    return children


def ol_to_html_node(i, blocks):
    """
    Converts ordered list blocks into an HTML ordered list node.

    Args:
        i (int): The current index in the list of blocks.
        blocks (list): The list of markdown blocks.

    Returns:
        tuple: The updated index and the HTML node representing the ordered list.
    """

    html_elements = []
    pattern = re.compile(r"^\d+\.\s")

    while i < len(blocks) and pattern.match(blocks[i]):
        block = blocks[i]
        children = text_to_children(block[2:].strip())
        li = ParentNode("li", children)
        html_elements.append(li)
        i += 1

    i -= 1
    return (i, ParentNode("ol", html_elements))


def ul_to_html_node(i, blocks):
    """
    Converts unordered list blocks into an HTML unordered list node.

    Args:
        i (int): The current index in the list of blocks.
        blocks (list): The list of markdown blocks.

    Returns:
        tuple: The updated index and the HTML node representing the unordered list.
    """

    html_elements = []
    pattern = re.compile(r"^[*]\s")

    while i < len(blocks) and pattern.match(blocks[i]):
        block = blocks[i]
        children = text_to_children(block[2:].strip())
        li = ParentNode("li", children)
        html_elements.append(li)
        i += 1

    i -= 1
    return (i, ParentNode("ul", html_elements))


def quote_to_html_node(block):
    """
    Converts a blockquote block into an HTML blockquote node.

    Args:
        block (str): The markdown block representing the blockquote.

    Returns:
        ParentNode: The HTML node representing the blockquote.
    """

    fragments = block.split("\n")
    lines = []

    for fragment in fragments:
        if not fragment.startswith(">"):
            raise ValueError("Invalid markdown")

        lines.append(fragment[1:].strip())

    content = " ".join(lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def code_to_html_node(block):
    """
    Converts a code block into an HTML pre/code node.

    Args:
        block (str): The markdown block representing the code.

    Returns:
        ParentNode: The HTML node representing the pre/code.
    """

    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def heading_to_html_node(block):
    """
    Converts a heading block into an HTML heading node.

    Args:
        block (str): The markdown block representing the heading.

    Returns:
        ParentNode: The HTML node representing the heading.
    """

    level = len(re.match(r"^\s*#{1,6}\s", block).group().strip())
    text = block[level + 1 :].strip()
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def paragraph_to_html_node(block):
    """
    Converts a paragraph block into an HTML paragraph node.

    Args:
        block (str): The markdown block representing the paragraph.

    Returns:
        ParentNode: The HTML node representing the paragraph.
    """

    lines = block.split("\n")
    joined = " ".join(lines)
    children = text_to_children(joined)
    return ParentNode("p", children)
