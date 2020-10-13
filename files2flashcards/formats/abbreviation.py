def extract(root):
    """Simple function for extracting abbreviation data"""

    return {"Full": root.attrib["title"], "Context": root.attrib["data-context"], "Abbreviation": root.text}

definition = {
    "tag": "abbr",
    "class_name": "h-fcard",
    "note_type": "Abbreviation",
    "mapping_function": extract
}