import re
import xml.etree.ElementTree as ET

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

    root.attrib["data-anki-id"] = str(id)

    return ET.tostring(root, encoding="unicode")