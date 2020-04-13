import re
import xml.etree.ElementTree as ET

mapping_registry = []

def find_fragments(raw_string, tag):
    """Find HTML fragments by tag.
    
    Returns a list of strings containing the fragments"""
    
    regex = "(?s)" + "<" + tag + ".*?</" + tag + ">"
    return re.findall(regex, raw_string)

def extract_abbreviation(root):
    """Simple function for extracting abbreviation data"""

    return {"full": root.attrib["title"], "context": root.attrib["data-context"], "abbreviation": root.text}

def inject_Anki_ID(root, id):
    """Inject an Anki ID into fragment"""

    root.attrib["data-anki-id"] = str(id)

    return root

def add_format(tag, class_name, mapping_function):
    mapping_registry.append({
        "tag": tag,
        "class_name": class_name,
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
                    data = extract_abbreviation(root)
                    root = inject_Anki_ID(root, 1234)

                    new_fragment = ET.tostring(root, encoding="unicode")

                    content = content.replace(fragment, new_fragment)

        f.seek(0)
        f.write(content)