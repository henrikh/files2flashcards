def extract(root):
    """Simple function for extracting synonym lists"""

    max_cloze_id = 0
    for child in root:
        if 'data-id' in child.attrib:
            max_cloze_id = max(max_cloze_id, int(child.attrib['data-id']))

    output = "Synonyms of"

    for child in root:
        if 'data-id' in child.attrib:
            cloze_id = int(child.attrib['data-id'])
        else:
            max_cloze_id = max_cloze_id + 1
            cloze_id = max_cloze_id
            child.attrib['data-id'] = str(cloze_id)

        output = output + "<br />{{c" + str(cloze_id) + "::" + child.text + "}}"

    return {"Text": output, "Extra": ""}

definition = {
    "tag": "ul",
    "class_name": "e-synonyms",
    "note_type": "Cloze",
    "mapping_function": extract
}