import re
import xml.etree.ElementTree as ET
import AnkiConnectWrapper
import os

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
    with open(path, 'r+') as f:
        content = f.read()

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

def process_files(path):
    for file in os.listdir(path):
        process_file(path + "/" + file)