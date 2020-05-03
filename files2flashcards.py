import re
import xml.etree.ElementTree as ET
import AnkiConnectWrapper
import os

taboo_word = None

mapping_registry = []

def find_fragments(raw_string, tag):
    """Find HTML fragments by tag.
    
    Returns a list of strings containing the fragments"""
    
    regex = "(?s)" + "<" + tag + ".*?</" + tag + ">"
    return re.findall(regex, raw_string)

def extract_abbreviation(root):
    """Simple function for extracting abbreviation data"""

    return {"Full": root.attrib["title"], "Context": root.attrib["data-context"], "Abbreviation": root.text}

def extract_abbreviation_basic(root):
    """Simple function for extracting abbreviation data"""

    return {"Back": root.attrib["title"], "Front": root.text}

def extract_cloze(root):
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

def inject_Anki_ID(root, id):
    """Inject an Anki ID into fragment"""

    root.attrib["data-anki-id"] = str(id)

    return root

def add_format(tag, class_name, note_type, mapping_function):
    mapping_registry.append({
        "tag": tag,
        "class_name": class_name,
        "note_type": note_type,
        "mapping_function": mapping_function
    })

def process_file(path):
    with open(path, 'r+', encoding='utf-8') as f:
        content = f.read()

        if taboo_word is not None and taboo_word in content:
            return

        print(path)

        for mapping in mapping_registry:
            fragments = find_fragments(content, mapping["tag"])
            for fragment in fragments:
                root = ET.fromstring(fragment)
                if "class" in root.attrib and mapping["class_name"] in root.attrib['class']:
                    data = mapping["mapping_function"](root)

                    if 'data-anki-id' in root.attrib:
                        AnkiConnectWrapper.update_note(root.attrib['data-anki-id'], data)
                    else:
                        note_id = AnkiConnectWrapper.add_note(mapping["note_type"], data)

                        root = inject_Anki_ID(root, note_id)

                    new_fragment = ET.tostring(root, encoding="unicode")

                    content = content.replace(fragment, new_fragment)

                    # TODO: What happens if a request fails?
                    f.seek(0)
                    f.write(content)

def process_folder(path, regex=r''):
    for file in os.listdir(path):
        if re.search(regex, file) is not None:
            process_file(path + "/" + file)