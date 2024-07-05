import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLNode(props={"class": "container", "id": "main"})
        self.assertEqual(node1.props_to_html(), 'class="container" id="main"')

        node2 = HTMLNode(props={"href": "https://www.example.com", "target": "_blank"})
        self.assertEqual(node2.props_to_html(), 'href="https://www.example.com" target="_blank"')
