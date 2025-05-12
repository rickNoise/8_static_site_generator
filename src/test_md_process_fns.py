import unittest

from md_process_fns import split_nodes_delimiter, split_string_by_delimiter, delim_index_builder
from textnode import TextNode, TextType
from md_process_fns import extract_markdown_images, extract_markdown_links
from md_process_fns import split_nodes_image, split_nodes_link

class TestDelimIndexBuilder(unittest.TestCase):
    def test_delim_index_builder(self):
        text = "012**b**89"
        delimiter = "**"
        exp_out = [ (3, 4), (6, 7) ]
        self.assertEqual(
            delim_index_builder(text, delimiter),
            exp_out
        )
    
    def test_delim_index_builder_2(self):
        text = "**b**"
        delimiter = "**"
        exp_out = [ (0, 1), (3, 4) ]
        self.assertEqual(
            delim_index_builder(text, delimiter),
            exp_out
        )
     
    def test_delim_index_builder_empty_text(self):
        text = ""
        delimiter = "**"
        exp_out = []
        self.assertEqual(
            delim_index_builder(text, delimiter),
            exp_out
        )
    
    def test_delim_index_builder_empty_delimiter(self):
        text = "this is text"
        delimiter = ""
        exp_out = []
        with self.assertRaises(Exception) as context:
            delim_index_builder(text, delimiter)
        self.assertEqual(str(context.exception), "delimiter must be a non-empty string")

class TestSplitStringByDelimiter(unittest.TestCase):
    def test_split_delimiter_length_2(self):
        text = "01**b**78"
        delimiter = "**"
        self.assertEqual(
            split_string_by_delimiter(text, delimiter),
            [
                {
                    "text": "01",
                    "was_delimited": False
                },
                {
                    "text": "b",
                    "was_delimited": True
                },
                {
                    "text": "78",
                    "was_delimited": False
                }
            ]
        )

    def test_split_empty_delimiter(self):
        text = "some text"
        delimiter = ""
        with self.assertRaises(Exception) as context:
            split_string_by_delimiter(text, delimiter)
        self.assertEqual(str(context.exception), "delimiter must be a non-empty string")

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
        node1 = TextNode("This is **text** with a `code block` word", TextType.TEXT)
        node2 = TextNode("bolded string", TextType.BOLD)
        node3 = TextNode("This is **another** string with **bold**", TextType.TEXT)
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

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )
    
class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        )
    
    def test_extract_markdown_links_ignoring_images(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev). This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_links(text),
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        )

class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        expected_output = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(
            new_nodes,
            expected_output
        )
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected_output = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertListEqual(
            new_nodes,
            expected_output
        )


if __name__ == "__main__":
    unittest.main()