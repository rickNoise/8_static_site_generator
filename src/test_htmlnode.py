import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from htmlnode import text_node_to_html_node
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node_test_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node_expected_output = ' href="https://www.google.com" target="_blank"'
        node = HTMLNode(props=node_test_props)
        self.assertEqual(node.props_to_html(), node_expected_output)

        node2_test_props = {
            "class": "fit-picture",
            "alt": "Grapefruit slice atop a pile of other slices"
        }
        node2_expected_output = ' class="fit-picture" alt="Grapefruit slice atop a pile of other slices"'
        node2 = HTMLNode(props=node2_test_props)
        self.assertEqual(node2.props_to_html(), node2_expected_output)

        node3_test_props = {
            "type": "button"
        }
        node3_expected_output = ' type="button"'
        node3 = HTMLNode(props=node3_test_props)
        self.assertEqual(node3.props_to_html(), node3_expected_output)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        test_props = {
            "href": "https://www.google.com"
        }
        node = LeafNode("a", "this is a link", test_props)
        expected_output = '<a href="https://www.google.com">this is a link</a>'
        self.assertEqual(node.to_html(), expected_output)
    
    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Heading 1", None)
        self.assertEqual(node.to_html(), "<h1>Heading 1</h1>")
    
    def test_parent_to_html_basic1(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected_out = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected_out)
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_none_children(self):
        parent_node = ParentNode("a", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()

    def test_to_html_with_empty_children_list(self):
        parent_node = ParentNode("a", [])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()

    def test_to_html_with_invalid_children_type(self):
        parent_node = ParentNode("a", "this is not a list")
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()

    def test_text_node_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_text_node_link(self):
        node = TextNode("This is a link text node", TextType.LINK, url="www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(
            html_node.props, 
            { "href": "www.google.com" }
        )
        self.assertEqual(
            html_node.to_html(), 
            '<a href="www.google.com">This is a link text node</a>'
        )

if __name__ == "__main__":
    unittest.main()