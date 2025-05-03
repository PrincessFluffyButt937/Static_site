import re

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def markdown_to_blocks(markdown):
    split_list = markdown.split("\n\n")
    new_list = []
    for element in split_list:
        element = element.strip()
        if element:
            if "\n" in element:
                new_elements = element.split("\n")
                new_list.append("\n".join([el.strip() for el in new_elements]))
                continue
            else:
                new_list.append(element.strip())
    return new_list

def extract_title(markdown):
    result = ""
    for line in markdown.splitlines():
        line = line.strip()
        if line:
            if line.startswith("# "):
                result = line.lstrip("# ")
                break
    if not result:
        raise Exception("No title was found.")
    else:
        return result