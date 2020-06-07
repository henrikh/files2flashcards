import xml.etree.ElementTree as ET

def extract(root):
    """Extract syntax definitions for programming languages"""

    body = ET.tostring(root[1][0], encoding='unicode')
    body = body[5:-6]

    return {"Meaning": root[0].text, "Syntax": body, "Language": root.attrib["data-language"]}

definition = {
    "tag": "dl",
    "class_name": "e-programming-syntax",
    "note_type": "Programming syntax",
    "mapping_function": extract
}