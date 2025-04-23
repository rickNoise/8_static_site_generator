import unittest

from md_process_fns import split_nodes_delimiter, split_string_by_delimiter
from textnode import TextNode, TextType


class TestSplitStringByDelimiter(unittest.TestCase):
    def test_split_empty_text(self):
        text = ""
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
    pass

if __name__ == "__main__":
    unittest.main()