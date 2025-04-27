
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6

def block_to_block_type(block):
    if is_heading(block):
        return BlockType.HEADING
    if is_code(block):
        return BlockType.CODE
    if is_quote(block):
        return BlockType.QUOTE
    if is_unordered(block):
        return BlockType.UNORDERED_LIST
    if is_ordered(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

# helper functions for block_to_block_type()

def is_code(block):
    lines = block.split("\n")
    if len(lines) < 2:  # Need at least opening and closing lines
        return False
    if lines[0] != "```" or lines[-1] != "```":
        return False
    return True

def is_quote(block):
    lines = block.split("\n")
    for line in lines:
        if not line.startswith(">"):
            return False
    return True

def is_unordered(block):
    lines = block.split("\n")
    for line in lines:
        if not line.startswith("- "):
            return False
    return True

def is_heading(block):
    if not block.startswith('#'):
        return False
    i = 0
    while i < len(block) and i < 6 and block[i] == "#":
        i += 1
    if i < len(block) and block[i] == " ":
        return True
    return False

def is_ordered(block):
    counter = 1
    spl_blocks = block.split("\n")
    for line in spl_blocks:
        if line.startswith(f"{counter}. "):
            counter += 1
            continue
        else:
            return False
    return True