import unittest
from inline_markdown import split_node_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, text_type_text, text_type_bold

class TestInlineMarkdown(unittest.TestCase):
    def test_delimit_bold(self):
        node = TextNode("Hello is text with **bolded** word", text_type_text)
        new_nodes = split_node_delimiter([node], "**", text_type_bold)
        self.assertListEqual([
            TextNode("Hello is text with ", text_type_text),
            TextNode("bolded", text_type_bold),
            TextNode(" word", text_type_text)
        ], new_nodes)

    def test_delimit_invalid(self):
        node = TextNode("Hello is text with **bolded word", text_type_text)
        with self.assertRaisesRegex(ValueError, 'Invalid markdown'):
            split_node_delimiter([node], "**", text_type_bold)

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

if __name__ == "__main__":
    unittest.main()
