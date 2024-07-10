import re

from htmlnode import HTMLNode


block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quota = "quota"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_block(markdown):
    fragments = markdown.split("\n")
    blocks = []

    for fragment in fragments:
        if fragment == "":
            continue

        blocks.append(fragment.strip())


    return blocks

def block_to_block_type(block):
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
    blocks = markdown_to_block(markdown)
    root = HTMLNode(tag="div", children=[])
    i = 0

    while i < len(blocks):
        block = blocks[i]
        block_type = block_to_block_type(block)

        if block_type == block_type_heading:
            heading_level = len(re.match(r"^\s*#{1,6}\s", block).group(0).strip())
            block_node = HTMLNode(tag=f"h{heading_level}", value=re.sub(r"^\s*#{1,6}\s", "", block))
        elif block_type == block_type_code:
            block_node = HTMLNode(tag="code", children=[HTMLNode(tag="pre", value=re.sub(r"```", "", block))])
        elif block_type == block_type_quota:
            block_node = HTMLNode(tag="blockquote", value=re.sub(r"^>\s", "", block))
        elif block_type == block_type_unordered_list:
            block_node = HTMLNode(tag="ul", children=[])

            while i < len(blocks) and block_to_block_type(blocks[i]) == block_type_unordered_list:
                line = blocks[i]
                block_node.children.append(HTMLNode(tag="li", value=re.sub(r"^[*-]\s", "", line)))
                i += 1

            i -= 1
        elif block_type == block_type_ordered_list:
            block_node = HTMLNode(tag="ol", children=[])

            while i < len(blocks) and block_to_block_type(blocks[i]) == block_type_ordered_list:
                line = blocks[i]
                block_node.children.append(HTMLNode(tag="li", value=re.sub(r"^\d+\.\s", "", line)))
                i += 1

            i -= 1
        else:
            block_node = HTMLNode(tag="p", value=block)

        i += 1
        root.children.append(block_node)

    return root
