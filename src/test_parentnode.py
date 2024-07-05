import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = ParentNode(tag="div", props={"class": "container"}, children=[
            LeafNode(tag="p", value="Hello, World!"),
            LeafNode(tag="strong", value="Goodbye, World!")
        ])

        self.assertEqual(node1.to_html(), '<div class="container"><p>Hello, World!</p><strong>Goodbye, World!</strong></div>')

        node2 = ParentNode(tag="ul", props={"class": "list"}, children=[
            LeafNode(tag="li", value="Item 1"),
            LeafNode(tag="li", value="Item 2"),
            LeafNode(tag="li", value="Item 3"),
        ])

        self.assertEqual(node2.to_html(), '<ul class="list"><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>')

    def raises_exception_props_to_html(self):
        with self.assertRaisesRegex(ValueError, "ParentNode must have a tag"):
            ParentNode(props="class=\"container\"", children=[
                LeafNode(tag="p", value="Hello, World!"),
                LeafNode(tag="strong", value="Goodbye, World!")
            ])

        with self.assertRaisesRegex(ValueError, "ParentNode must have children"):
            ParentNode(tag="ul", children=[])
