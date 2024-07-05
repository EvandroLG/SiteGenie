import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = LeafNode(props={"class": "container", "id": "main"})
        self.assertEqual(node1.props_to_html(), 'class="container" id="main"')

        node2 = LeafNode(props={"href": "https://www.example.com", "target": "_blank"})
        self.assertEqual(node2.props_to_html(), 'href="https://www.example.com" target="_blank"')

    def test_to_html(self):
        node = LeafNode("a", "Click me", {"href": "https://www.example.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.example.com" target="_blank">Click me</a>')
