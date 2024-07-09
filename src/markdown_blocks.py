import re


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
