import unittest

from md_process_fns import split_nodes_delimiter, split_string_by_delimiter
from textnode import TextNode, TextType


class TestSplitStringByDelimiter(unittest.TestCase):
    def test_split_empty_text(self):
        text = ""
        delimiter = "`"
        self.assertEqual(
            split_string_by_delimiter(text, delimiter),
            []
        )
    
    def test_split_with_no_delimiter_found(self):
        text = "this has no delimiter"
        delimiter = "`"
        self.assertEqual(
            split_string_by_delimiter(text, delimiter),
            [
                {
                    "text": text,
                    "was_delimited": False
                }
            ]
        )
    
    def test_split_with_only_delimiters_found_single(self):
        text = "``"
        delimiter = "`"
        self.assertEqual(
            split_string_by_delimiter(text, delimiter),
            []
        )
    
    def test_split_with_only_delimiters_found_double(self):
        text = "````"
        delimiter = "`"
        self.assertEqual(
            split_string_by_delimiter(text, delimiter),
            []
        )
    
    def test_split_unmatched_delimiter_single(self):
        text = "this has an `unmatched delimiter"
        delimiter = "`"
        self.assertRaises(
            Exception, 
            split_string_by_delimiter,
            text,
            delimiter
        )
    
    def test_split_unmatched_delimiter_triple(self):
        text = "this has an `unmatched` `delimiter"
        delimiter = "`"
        self.assertRaises(
            Exception, 
            split_string_by_delimiter,
            text,
            delimiter
        )
    
    def test_split_matched_delimiter_one_pair(self):
        text = "this has a single `matched` delimiter pair"
        delimiter = "`"
        self.assertEqual(
            split_string_by_delimiter(text, delimiter),
            [
                {
                    "text": "this has a single ",
                    "was_delimited": False
                },
                {
                    "text": "matched",
                    "was_delimited": True
                },
                {
                    "text": " delimiter pair",
                    "was_delimited": False
                }
            ]
        )

    def test_split_matched_delimiter_two_pair(self):
        text = "this has `two` matched `delimiter` pairs"
        delimiter = "`"
        self.assertEqual(
            split_string_by_delimiter(text, delimiter),
            [
                {
                    "text": "this has ",
                    "was_delimited": False
                },
                {
                    "text": "two",
                    "was_delimited": True
                },
                {
                    "text": " matched ",
                    "was_delimited": False
                },
                {
                    "text": "delimiter",
                    "was_delimited": True
                },
                {
                    "text": " pairs",
                    "was_delimited": False
                }
            ]
        )

    def test_split_delimiter_on_entire_text(self):
        text = "`whole text is surrounded`"
        delimiter = "`"
        self.assertEqual(
            split_string_by_delimiter(text, delimiter),
            [
                {
                    "text": "whole text is surrounded",
                    "was_delimited": True
                }
            ]
        )
    
class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_node_bootdev_example(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )
    
    def test_split_node_many_inputs_italic(self):
        node1 = TextNode("This is _text_ with a `code block` word", TextType.TEXT)
        node2 = TextNode("italicised string", TextType.ITALIC)
        node3 = TextNode("This is _another_ string with _italics_", TextType.TEXT)
        new_nodes = split_nodes_delimiter(
            [ node1, node2, node3 ],
            "_",
            TextType.ITALIC
        )
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.ITALIC),
                TextNode(" with a `code block` word", TextType.TEXT),
                TextNode("italicised string", TextType.ITALIC),
                TextNode("This is ", TextType.TEXT),
                TextNode("another", TextType.ITALIC),
                TextNode(" string with ", TextType.TEXT),
                TextNode("italics", TextType.ITALIC),
            ]
        )
    
    def test_split_node_many_inputs_bold(self):
        node1 = TextNode("This is *text* with a `code block` word", TextType.TEXT)
        node2 = TextNode("bolded string", TextType.BOLD)
        node3 = TextNode("This is *another* string with *bold*", TextType.TEXT)
        new_nodes = split_nodes_delimiter(
            [ node1, node2, node3 ],
            "**",
            TextType.BOLD
        )
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with a `code block` word", TextType.TEXT),
                TextNode("bolded string", TextType.BOLD),
                TextNode("This is ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
                TextNode(" string with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ]
        )

if __name__ == "__main__":
    unittest.main()