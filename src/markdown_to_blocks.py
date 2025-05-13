def markdown_to_blocks(markdown):
    """
    It takes a raw Markdown string (representing a full document) as input and returns a list of "block" strings. 
    The example below would be split into three strings:

    # This is a heading

    This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

    - This is the first list item in a list block
    - This is a list item
    - This is another list item

    The .split() method can be used to split a string into blocks based on a delimiter (\n\n is a double newline).
    You should .strip() any leading or trailing whitespace from each block.
    Remove any "empty" blocks due to excessive newlines.
    """

    blocks = markdown.split("\n\n")
    print(f"blocks pre prcoessing: {blocks}")
    for i in range(len(blocks)):
        print(f"current block reviewed... {blocks[i]}")
        blocks[i] = blocks[i].strip()
    for block in blocks:
        if not block:
            blocks.remove(block)

    print(f"returning blocks: {blocks}")
    return blocks
