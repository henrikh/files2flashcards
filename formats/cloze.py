def extract(root):
    """Simple function for extracting cloze deletion data"""

    max_cloze_id = 0
    for child in root:
        if 'data-id' in child.attrib:
            max_cloze_id = max(max_cloze_id, int(child.attrib['data-id']))

    output = ""
    if root.text is not None:
        output = root.text

    for child in root:
        tail = ""
        if child.tail is not None:
            tail = child.tail

        if 'data-id' in child.attrib:
            cloze_id = int(child.attrib['data-id'])
        else:
            max_cloze_id = max_cloze_id + 1
            cloze_id = max_cloze_id
            child.attrib['data-id'] = str(cloze_id)

        output = output + "{{c" + str(cloze_id) + "::" + child.text + "}}" + tail

    return {"Text": output, "Extra": ""}

definition = {
    "tag": "span",
    "class_name": "e-cloze",
    "note_type": "Cloze",
    "mapping_function": extract
}