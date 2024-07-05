import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node_1 = TextNode("Hello", "Greeting", "https://www.example.com")
        node_2 = TextNode("Hello", "Greeting", "https://www.example.com")
        self.assertEqual(node_1, node_2)

if __name__ == "__main__":
    unittest.main()
