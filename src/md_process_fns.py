from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    It takes a list of "old nodes", a delimiter, and a text type. It should return a new list of nodes, where any "text" type nodes in the input list are (potentially) split into multiple nodes based on the syntax. 
    
    For example, given the following input:
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    new_nodes becomes:
    [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
    ]
    """

    # iterate through old_nodes, ignoring any that are not TextType.TEXT
    # process TEXT nodes by trawling through text for the delimiter, and pulling out any content until the next delimiter
    # if not matching delimiter is found, raise Exception
    # consider multiple pairs of delimiters within the same text string
    # write test cases
    
    if not old_nodes: # if input list is empty, just return it
        return old_nodes
    
    return_lst = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            return_lst.append(node)
        else:
            processed_text = split_string_by_delimiter(node.text, delimiter)
            for obj in processed_text:
                return_lst.append(
                    TextNode(
                        obj["text"],
                        text_type if obj["was_delimited"] == True else TextType.TEXT 
                    )
                )
    return return_lst

# helper fn for split_nodes_delimiter
def split_string_by_delimiter(text, delimiter):
    # input 'text': a string; 'delimiter': a string
    # output: a list of objects of the form:
    # { "text": "slice of text", "was_delimited": bool }
    # "was_delimited" tells you whether or not that slice was surrounded by delimiters
    # delimiter characters are excluded for text slices
    # empty slices are ignored and thrown away in all instances
    # raise Exception if there is unmatched delimiter(s)
    
    if not text: # if input is the empty string
        return []

    # if the delimiter string is empty or not a string
    if len(delimiter) == 0 or not isinstance(delimiter, str):
        raise Exception("delimiter must be a non-empty string")

    try:
        delimiter_indexes = delim_index_builder(text, delimiter)
    except Exception as delim_index_builder_exception:
        raise delim_index_builder_exception

    # check for case of finding no delimiters
    if not delimiter_indexes:
        return [
            {
                "text": text,
                "was_delimited": False
            }
        ]

    # check for unmatched delimiter chars
    if len(delimiter_indexes) % 2 != 0:
        raise Exception("Unmatched delimiter! Formatting issue with input text.")

    return_lst = [] 
    # add the slice (if any) up to the first delimiter
    if delimiter_indexes[0][0] > 0:
        return_lst.append(
            {
                "text": text[:delimiter_indexes[0][0]],
                "was_delimited": False
            }
        )
    # iterate through delimiter_indexes, excluding the last one
    for i in range(len(delimiter_indexes) - 1):
        starting_char = delimiter_indexes[i][1] + 1 #start at the character after the end of the first delimiter 
        ending_char = delimiter_indexes[i + 1][0] #end at the first index of the next delimiter
        text_slice = text[ starting_char : ending_char ]
        if text_slice:
            was_delimited = (i % 2 == 0)
            return_lst.append(
                {
                    "text": text_slice,
                    "was_delimited": was_delimited
                }
            )
    # add the slice of remaining text after last delimiter
    if delimiter_indexes[-1][1] != len(text) - 1:
        starting_char = delimiter_indexes[-1][1] + 1
        return_lst.append(
            {
                "text": text[starting_char:],
                "was_delimited": False
            }
        )

    return return_lst

# helper fn for split_string_by_delimiter
def delim_index_builder(text, delimiter):
    """
    inputs -> text: str, delimiter: str
    output -> index_list: list of tuples
    each item in the list represents an occurence of the delimiter in the text string
    the first int in the tuple is the char index in the string in which the delimiter starts
    the second int in the tuple is the char index in the string in which the delimiter ends
    e.g. if the text is "012**b**89" and the delimiter is "**"
    ---> output should be: [(3, 4), (6, 7)]
    Assume the delimiter is a string and is not empty.
    """
    if len(delimiter) == 0 or not isinstance(delimiter, str):
        raise Exception("delimiter must be a non-empty string")
    delimiter_length = len(delimiter)
    delimiter_indexes = []
    for idx in range(len(text) - (delimiter_length - 1)):
        if text[idx:idx+delimiter_length] == delimiter:
            delimiter_indexes.append(
                (idx, idx+delimiter_length - 1)
            )
    return delimiter_indexes

def extract_markdown_images(text):
    """
    Create a function extract_markdown_images(text) that takes raw markdown text 
    and returns a list of tuples.
    Each tuple should contain the alt text and the URL of any markdown images.
    For example:
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(text))
    # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    """
    matches = re.findall(r"\!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    """
    Create a similar function extract_markdown_links(text) that extracts markdown links instead of images. 
    It should return tuples of anchor text and URLs.
    For example:
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_links(text))
    # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
    """
    matches = re.findall(r"(?<!\!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    if not old_nodes:
        return old_nodes
    
    return_lst = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            return_lst.append(node)
        else:
            matches = extract_markdown_images(node.text)
            # if the text node has no images in it, just append it as is
            if len(matches) == 0:
                return_lst.append(node)
            # if it does have images in it, process differently
            else:
                processed_nodes = recursive_match_processing(matches, node.text, [])
                print(f"processed_nodes: {processed_nodes}")
                for item in processed_nodes:
                    return_lst.append(item)

    print(f"about to return return_lst: {return_lst}")
    return return_lst

# helper fn for split_nodes_image
def recursive_match_processing(matches, text, output_list=[]):
    print(f"entering into recursive_match_processing... with matches: {matches} and remaining_text: {text}")
    # returns an array of TextNodes
    
    # base case
    if len(matches) == 0:
        return output_list

    # recursive case
    match = matches[0]
    print(f"processing match: {match}")
    split_text = text.split(f"![{match[0]}]({match[1]})", 1)
    print(f"split_text is: {split_text}")

    # create a Text type TextNode for the initial text before the image
    if split_text[0] != "":
        output_list.append(
            TextNode(split_text[0], TextType.TEXT)
        )
    
    # create an Image type TextNode for the image itself
    output_list.append(
        TextNode(match[0], TextType.IMAGE, match[1])
    )
    # if there are remaining matches after this one, run again recursively
    if len(matches) > 1:
        remaining_matches = matches[1:]
        if len(split_text) > 1:
            remaining_text = split_text[1]
        else:
            remaining_text = ""
        print(f"about to recurse with current output_list: {output_list}")
        output_list.extend(recursive_match_processing(remaining_matches, remaining_text, []))
        return output_list
    # if no remaining matches after this one
    else:
        # covers the trailing text left after the last image match
        if len(split_text) > 1 and len(split_text[1]) > 0:
            output_list.append(
                TextNode(split_text[1], TextType.TEXT)
            )
        print(f"about to return output_list: {output_list}")
        return output_list

def split_nodes_link(old_nodes):
    pass