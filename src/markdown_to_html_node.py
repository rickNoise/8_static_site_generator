from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes
from htmlnode import HTMLNode, ParentNode, LeafNode, text_node_to_html_node
from markdown_to_blocks import markdown_to_blocks
from block_to_block_type import block_to_block_type, BlockType
import pprint


def __main__():
    md = """
This is **bolded with _italics section_ inside the bold** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
    print(markdown_to_html_node(md))


def markdown_to_html_node(markdown):
    # Converts a full markdown document into a single parent HTMLNode. 
    # That one parent HTMLNode should (obviously) contain many child HTMLNode objects representing the nested elements.
    print(f"\n>>>>> STARTING markdown_to_html_node with input: {markdown}")

    # 1. Convert raw markdown input into "blocks" (strings)
    blocks = markdown_to_blocks(markdown)
    print(f"\n{'\033[36m'}>>>>> PROCESSED markdown into blocks:{'\033[0m'}")
    pprint.pp(blocks)

    # 2. Loop over the blocks
    #   a. determine the block type
    #   b. create a new html node with the proper data, based on block type
    #   c. assign proper child HTMLNode objects to the block node
    print(f"\n>>>>> PROCESSING blocks")
    for block in blocks:
        print(f"\n>>>>> PROCESSING block:")
        pprint.pp(block)
        block_type = block_to_block_type(block)
        print(f"block_type determined to be: {block_type}")

        html_node = block_to_html_node(block, block_type)

    
    # 3. Make all block nodes children under a single parent HTMLNode 
    # (which should just be a div) and return it



def block_to_html_node(block, block_type):
    print(f"\n>>>>> PROCESSING block_to_html_node with block {block} and block_type{block_type}")
    # takes a block (string) and a block_type (BlockType enum)
    # returns an HTMLNode

    child_node_list = text_to_children(block)
    print(f"\n>>>>> PROCESSED child_node_list: {child_node_list}")


    match block_type:
        case BlockType.HEADING:
            pass
        case BlockType.CODE:
            pass
        case BlockType.QUOTE:
            pass
        case BlockType.UNORDERED_LIST:
            pass
        case BlockType.ORDERED_LIST:
            pass
        case BlockType.PARAGRAPH:
            pass
        case _:
            raise Exception("block_type input is not correct BlockType enum value")


def text_to_children(text):
    # takes string
    # outputs a nested list of HTMLNodes
    initial_text_array = [text]
    return_array = []

    textnode_array = text_to_textnodes(text)
    print(f"\n>>>>> PROCESSED textnode_array:")
    pprint.pp(textnode_array)
    for text_node in textnode_array:
        if text_node.text_type == TextType.TEXT:
            return_array.append(LeafNode(None, text_node.text))

    print(f">>>>> the return array")
    pprint.pp(return_array)
    return return_array

if __name__ == '__main__':
    __main__()
