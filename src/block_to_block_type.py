from enum import Enum
import re

BlockType = Enum(
    'BlockType', [
        'PARAGRAPH',
        'HEADING',
        'CODE',
        'QUOTE',
        'UNORDERED_LIST',
        'ORDERED_LIST',
    ]
)

def block_to_block_type(markdown):
    """
    Takes a single block of markdown text as input and returns the BlockType representing the type of block it is. 
    You can assume all leading and trailing whitespace were already stripped (we did that in a previous lesson).
    
    Headings start with 1-6 # characters, followed by a space and then the heading text.
    Code blocks must start with 3 backticks and end with 3 backticks.
    Every line in a quote block must start with a > character.
    Every line in an unordered list block must start with a - character, followed by a space.
    Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
    If none of the above conditions are met, the block is a normal paragraph.
    """

    markdown_split_by_line = markdown.split("\n")
    print(f"markdown_split_by_line: {markdown_split_by_line}")

    if test_for_heading(markdown):
        return BlockType.HEADING
    elif test_for_code(markdown):
        return BlockType.CODE
    elif test_for_quote(markdown_split_by_line):
        return BlockType.QUOTE
    elif test_for_unordered_list(markdown_split_by_line):
        return BlockType.UNORDERED_LIST
    elif test_for_ordered_list(markdown_split_by_line):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def test_for_heading(string):
    regex = r"^#{1,6} .*$"
    return re.match(regex, string)

def test_for_code(markdown):
    if markdown[0:3] == "```" and markdown[-3:] == "```":
        return True
    else:
        return False

def test_for_quote(array):
    for str in array:
        if str[0] != ">":
            return False
    return True

def test_for_unordered_list(array):
    for str in array:
        if str[0:2] != "- ":
            return False
    return True

def test_for_ordered_list(array):
    preceeding_numeral = 0
    pattern = r"^(\d+)\. (.*)$"  # Regex to match: one or more digits, a period, a space, and then anything

    for str in array:
        match = re.match(pattern, str)
        print(f"match :: {match}")
        if not match:
            return False
        
        try:
            print(f"the first match group is {match.group(1)}") # Extract the first capturing group (the digits)
            current_numeral = int(match.group(1))
            if current_numeral != preceeding_numeral + 1:
                return False
            preceeding_numeral = current_numeral
        except:
            return False
        
    return True