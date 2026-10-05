from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    final_blocks = []
    for block in blocks:
        if block.isspace() or block == "":
            continue
        final_blocks.append(block.strip())
    
    return final_blocks

def block_to_block_type(text: str) -> BlockType:
    if text.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif text.startswith("```") and text.endswith("```"):
        return BlockType.CODE

    lines = text.split("\n")
    i = 0
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif all(line.startswith(f"{i}. ") for line in lines if (i := i + 1)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH