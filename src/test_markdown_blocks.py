import unittest

from markdown_blocks import (
    markdown_to_block,
    block_to_block_type,
    block_type_heading,
    block_type_code,
    block_type_quota,
    block_type_unordered_list,
    block_type_ordered_list,
    block_type_paragraph,
    markdown_to_html_node
)

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_block(self):
        markdown = """This is **bolded** paragraph

        This is another paragraph with *italic* text and `code` here
        This is the same paragraph on a new line

        * This is a list
        * with items"""

        blocks = markdown_to_block(markdown)

        self.assertListEqual([
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here",
            "This is the same paragraph on a new line",
            "* This is a list",
            "* with items"
        ], blocks)

    def test_block_type_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)

        block = "## This is a heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)

        block = "### This is a heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)

        block = "#### This is a heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)

        block = "##### This is a heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)

        block = "###### This is a heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)

    def test_block_type_code(self):
        block = "```python```"
        self.assertEqual(block_to_block_type(block), block_type_code)

        block = "```rubby```"
        self.assertEqual(block_to_block_type(block), block_type_code)

    def test_block_type_quota(self):
        block = "> This is a quota"
        self.assertEqual(block_to_block_type(block), block_type_quota)

    def test_block_type_unordered_list(self):
        block = "* This is a list"
        self.assertEqual(block_to_block_type(block), block_type_unordered_list)

        block = "- This is a list"
        self.assertEqual(block_to_block_type(block), block_type_unordered_list)

    def test_block_type_ordered_list(self):
        block = "1. This is a list"
        self.assertEqual(block_to_block_type(block), block_type_ordered_list)

        block = "2. This is a list"
        self.assertEqual(block_to_block_type(block), block_type_ordered_list)

        block = "3. This is a list"
        self.assertEqual(block_to_block_type(block), block_type_ordered_list)

    def test_block_type_paragraph(self):
        block = "This is a paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_markdown_to_html_node(self):
        markdown = """# This is a heading

        This is a paragraph

        ```print("Hello, World!")```

        > This is a quota

        * This is a list
        * with items

        1. This is a list
        2. with items"""

        html_node = markdown_to_html_node(markdown)

        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 6)

        self.assertEqual(html_node.children[0].tag, "h1")
        self.assertEqual(html_node.children[0].value, "This is a heading")

        self.assertEqual(html_node.children[1].tag, "p")
        self.assertEqual(html_node.children[1].value, "This is a paragraph")

        self.assertEqual(html_node.children[2].tag, "code")
        self.assertEqual(html_node.children[2].children[0].tag, "pre")
        self.assertEqual(html_node.children[2].children[0].value, "print(\"Hello, World!\")")

        self.assertEqual(html_node.children[3].tag, "blockquote")
        self.assertEqual(html_node.children[3].value, "This is a quota")

        self.assertEqual(html_node.children[4].tag, "ul")
        self.assertEqual(len(html_node.children[4].children), 2)

        self.assertEqual(html_node.children[4].children[0].tag, "li")
        self.assertEqual(html_node.children[4].children[0].value, "This is a list")

        self.assertEqual(html_node.children[4].children[1].tag, "li")
        self.assertEqual(html_node.children[4].children[1].value, "with items")

        self.assertEqual(html_node.children[5].tag, "ol")
        self.assertEqual(len(html_node.children[5].children), 2)

        self.assertEqual(html_node.children[5].children[0].tag, "li")
        self.assertEqual(html_node.children[5].children[0].value, "This is a list")

        self.assertEqual(html_node.children[5].children[1].tag, "li")
        self.assertEqual(html_node.children[5].children[1].value, "with items")
