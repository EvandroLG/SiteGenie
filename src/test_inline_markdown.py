import unittest

from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
    extract_title,
    text_to_textnodes
)

from textnode import  (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_image,
    text_type_link
)

class TestInlineMarkdown(unittest.TestCase):
    def test_delimit_bold(self):
        node = TextNode("Hello is text with **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual([
            TextNode("Hello is text with ", text_type_text),
            TextNode("bolded", text_type_bold),
            TextNode(" word", text_type_text)
        ], new_nodes)

    def test_delimit_invalid(self):
        node = TextNode("Hello is text with **bolded word", text_type_text)
        with self.assertRaisesRegex(ValueError, 'Invalid markdown'):
            split_nodes_delimiter([node], "**", text_type_bold)

    def test_extract_markdown_images(self):
        text1 = "![Alt text](https://www.example.com/image.png)"
        self.assertListEqual([("Alt text", "https://www.example.com/image.png")], extract_markdown_images(text1))

        text2 = "This is a text ![Alt text](https://www.example.com/image.png) ![Alt text](https://www.example.com/image.png)"
        self.assertListEqual([
            ("Alt text", "https://www.example.com/image.png"),
            ("Alt text", "https://www.example.com/image.png")
        ], extract_markdown_images(text2))

        text3 = "This is just a text [Link text](https://www.example.com)"
        self.assertListEqual([], extract_markdown_images(text3))

    def test_extract_markdown_links(self):
        text1 = "[Link text](https://www.example.com)"
        self.assertListEqual([("Link text", "https://www.example.com")], extract_markdown_links(text1))

        text2 = "This is a text [Link text](https://www.example.com) [Link text](https://www.example.com)"
        self.assertListEqual([
            ("Link text", "https://www.example.com"),
            ("Link text", "https://www.example.com")
        ], extract_markdown_links(text2))

        text3 = "This is just a text ![Alt text](https://www.example.com/image.png)"
        self.assertListEqual([], extract_markdown_links(text3))

    def test_split_nodes_image(self):
        node1 = TextNode("Hello is text with ![Alt text](https://www.example.com/image.png)", text_type_text)
        self.assertListEqual([
            TextNode("Hello is text with ", text_type_text),
            TextNode("Alt text", text_type_image, "https://www.example.com/image.png")
        ], split_nodes_image([node1]))

        node2 = TextNode("Hello is text with ![Alt text 1](https://www.example.com/image1.png) ![Alt text 2](https://www.example.com/image2.png)", text_type_text)
        self.assertListEqual([
            TextNode("Hello is text with ", text_type_text),
            TextNode("Alt text 1", text_type_image, "https://www.example.com/image1.png"),
            TextNode(" ", text_type_text),
            TextNode("Alt text 2", text_type_image, "https://www.example.com/image2.png")
        ], split_nodes_image([node2]))

        node3 = TextNode("Hello is text with ![Alt text](https://www.example.com/image.png) and ![Alt text](https://www.example.com/image.png)", text_type_text)
        self.assertListEqual([
            TextNode("Hello is text with ", text_type_text),
            TextNode("Alt text", text_type_image, "https://www.example.com/image.png"),
            TextNode(" and ", text_type_text),
            TextNode("Alt text", text_type_image, "https://www.example.com/image.png")
        ], split_nodes_image([node3]))

    def test_split_nodes_link(self):
        node1 = TextNode("Hello is text with [Link text](https://www.example.com)", text_type_text)
        self.assertListEqual([
            TextNode("Hello is text with ", text_type_text),
            TextNode("Link text", text_type_link, "https://www.example.com")
        ], split_nodes_link([node1]))

        node2 = TextNode("Hello is text with [Link text 1](https://www.example.com) [Link text 2](https://www.example.com)", text_type_text)
        self.assertListEqual([
            TextNode("Hello is text with ", text_type_text),
            TextNode("Link text 1", text_type_link, "https://www.example.com"),
            TextNode(" ", text_type_text),
            TextNode("Link text 2", text_type_link, "https://www.example.com")
        ], split_nodes_link([node2]))

        node3 = TextNode("Hello is text with [Link text](https://www.example.com) and [Link text](https://www.example.com)", text_type_text)
        self.assertListEqual([
            TextNode("Hello is text with ", text_type_text),
            TextNode("Link text", text_type_link, "https://www.example.com"),
            TextNode(" and ", text_type_text),
            TextNode("Link text", text_type_link, "https://www.example.com")
        ], split_nodes_link([node3]))

    def test_text_to_textnodes(self):
        text = "Hello is text with ![Alt text](https://www.example.com/image.png) and [Link text](https://www.example.com)"
        nodes = text_to_textnodes(text)
        self.assertListEqual([
            TextNode("Hello is text with ", text_type_text),
            TextNode("Alt text", text_type_image, "https://www.example.com/image.png"),
            TextNode(" and ", text_type_text),
            TextNode("Link text", text_type_link, "https://www.example.com")
        ], nodes)

    def test_extract_title(self):
        text1 = "# This is a heading"
        self.assertEqual("This is a heading", extract_title(text1))

        text2 = """# This is a heading
        ## Introduction
        This is a simple markdown file."""
        self.assertEqual("This is a heading", extract_title(text2))

if __name__ == "__main__":
    unittest.main()
