import unittest

from htmlnode import HTMLNode


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

if __name__ == "__main__":
    unittest.main()