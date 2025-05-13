import unittest

from block_to_block_type import block_to_block_type, BlockType

class TestBlockToBlockType(unittest.TestCase):
    """
    Headings start with 1-6 # characters, followed by a space and then the heading text.
    Code blocks must start with 3 backticks and end with 3 backticks.
    Every line in a quote block must start with a > character.
    Every line in an unordered list block must start with a - character, followed by a space.
    Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
    If none of the above conditions are met, the block is a normal paragraph.
    """
    
    def test_block_to_block_type_paragraph(self):
        md = "This is a normal paragraph."
        output = block_to_block_type(md)
        expected_ouput = BlockType.PARAGRAPH
        self.assertEqual(
            output,
            expected_ouput
        )
    
    def test_block_to_block_type_heading(self):
        md = "### Heading 3"
        output = block_to_block_type(md)
        expected_ouput = BlockType.HEADING
        self.assertEqual(
            output,
            expected_ouput
        )

    def test_block_to_block_type_code(self):
        md = "```\nthis is a code block\n```"
        output = block_to_block_type(md)
        expected_ouput = BlockType.CODE
        self.assertEqual(
            output,
            expected_ouput
        )
    def test_block_to_block_type_quote(self):
        md = """> this is a quoted
>block
>with three lines"""
        output = block_to_block_type(md)
        expected_ouput = BlockType.QUOTE
        self.assertEqual(
            output,
            expected_ouput
        )

    def test_block_to_block_type_unordered_list(self):
        md = """- this is
- an unordered
- list with three items"""
        output = block_to_block_type(md)
        expected_ouput = BlockType.UNORDERED_LIST
        self.assertEqual(
            output,
            expected_ouput
        )

    def test_block_to_block_type_ordered_list(self):
        md = """1. this is an
2. ordered list
3. with many items
4. a
5. a
6. a
7. a
8. a
9. a
10. a
11. a"""
        output = block_to_block_type(md)
        expected_ouput = BlockType.ORDERED_LIST
        self.assertEqual(
            output,
            expected_ouput
        )