from textnode import TextNode, TextType

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



def split_string_by_delimiter(text, delimiter):
    # assumes delimiter is a single character!
    # input 'text': a string
    # output: a list of objects of the form:
    # { "text": "slice of text", "was_delimited": bool }
    # "was_delimited" tells you whether or not that slice was surrounded by delimiters
    # delimiter characters are excluded for text slices
    # empty slices are ignored and thrown away in all instances
    # raise Exception if there is unmatched delimiter(s)
    
    if not text: # if input is the empty string
        return []
    
    delimiter_indexes = []
    for idx in range(len(text)):
        if text[idx] == delimiter:
            delimiter_indexes.append(idx)

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
    if text[:delimiter_indexes[0]]:
        # print(f"leading text_slice to add: '{text[:delimiter_indexes[0]]}'")
        return_lst.append(
            {
                "text": text[:delimiter_indexes[0]],
                "was_delimited": False
            }
        )
    # iterate through every *other* index, slicing the text string 
    # between the index and the next index from the list of delimiter indexes
    # and adding the slice to the return_lst
    for i in range(0, len(delimiter_indexes) - 1):
        open_delim = delimiter_indexes[i]
        close_delim = delimiter_indexes[i+1]
        text_slice = text[ open_delim + 1 : close_delim ]
        if text_slice:
            was_delimited = (i % 2 == 0)
            # print(f"text_slice to append: '{text_slice}' with was_delimited: {was_delimited}")
            return_lst.append(
                {
                    "text": text_slice,
                    "was_delimited": was_delimited
                }
            )
    # add the slice of remaining text after last delimiter
    if text[delimiter_indexes[-1]+1:]:
        # print(f"trailing text_slice to add: '{text[delimiter_indexes[-1]+1:]}'")
        return_lst.append(
            {
                "text": text[delimiter_indexes[-1]+1:],
                "was_delimited": False
            }
        )

    return return_lst