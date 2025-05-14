from textnode import TextNode, TextType
from md_process_fns import *

def text_to_textnodes(text):
    # print(f"RUNNING TEXT_TO_TEXTNODES with input {text}")
    nodes = [TextNode(text, TextType.TEXT)]

    # BOLD text
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    # ITALIC text
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    # CODE text
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    # IMAGE text
    nodes = split_nodes_image(nodes)
    # LINK text
    nodes = split_nodes_link(nodes)

    return nodes