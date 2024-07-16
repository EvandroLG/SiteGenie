import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node_1 = TextNode("Hello", "Greeting", "https://www.example.com")
        node_2 = TextNode("Hello", "Greeting", "https://www.example.com")
        self.assertEqual(node_1, node_2)

    def test_to_html_node(self):
        link = TextNode("Hello", "link", "https://www.example.com")
        self.assertEqual(
            link.to_html_node().to_html(), '<a href="https://www.example.com">Hello</a>'
        )

        code = TextNode("print('Hello, World!')", "code", None)
        self.assertEqual(
            code.to_html_node().to_html(), "<code>print('Hello, World!')</code>"
        )

        bold = TextNode("Hello", "bold", None)
        self.assertEqual(bold.to_html_node().to_html(), "<b>Hello</b>")

        italic = TextNode("Hello", "italic", None)
        self.assertEqual(italic.to_html_node().to_html(), "<i>Hello</i>")


if __name__ == "__main__":
    unittest.main()
