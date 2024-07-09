import unittest

from markdown_blocks import (
    markdown_to_block,
    block_to_block_type,
    block_type_heading,
    block_type_code,
    block_type_quota,
    block_type_unordered_list,
    block_type_ordered_list,
    block_type_paragraph
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
