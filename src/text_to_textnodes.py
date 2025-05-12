from textnode import TextNode, TextType
from md_process_fns import *

def text_to_textnodes(text):
    print(f"RUNNING TEXT_TO_TEXTNODES with input {text}")
    starting_input = [TextNode(text, TextType.TEXT)]
    final_node_list = []

    # BOLD text
    final_node_list = split_nodes_delimiter(starting_input, "**", TextType.BOLD)
    # ITALIC text
    final_node_list = split_nodes_delimiter(final_node_list, "_", TextType.ITALIC)
    # CODE text
    final_node_list = split_nodes_delimiter(final_node_list, "`", TextType.CODE)

    # IMAGE text
    final_node_list = split_nodes_image(final_node_list)
    # LINK text
    final_node_list = split_nodes_link(final_node_list)

    print(f"about to return {final_node_list}")
    return final_node_list