import re
import xml.etree.ElementTree as ET
from files2flashcards import AnkiConnectWrapper
import os
import time
import json
import logging

taboo_word = None

mapping_registry = []

DATA_FILE = ".files2flashcards"

def find_fragments(raw_string, tag):
    """Find HTML fragments by tag.
    
    Returns a list of strings containing the fragments"""
    
    regex = "(?s)" + "<" + tag + ".*?</" + tag + ">"
    return re.findall(regex, raw_string)

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
    logging.info(f"Processing: {path}")
    with open(path, 'r+', encoding='utf-8') as f:
        content = f.read()

        if taboo_word is not None and taboo_word in content:
            return

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

                    f.seek(0)
                    f.write(content)

def process_folder(path, regex=r'', only_changed=False, data_file_dir=None):

    last_run = 0.0
    previous_processed_files = {}

    if data_file_dir is None:
        data_file_dir = path

    data_file_path = data_file_dir + "/" + DATA_FILE

    if only_changed and os.path.exists(data_file_path):
        with open(data_file_path, "r") as f:
            data = json.load(f)
            last_run = data['last_run']
            previous_processed_files = data['processed_files']

    current_run = time.time()
    current_processed_files = {}

    for file in os.listdir(path):
        file_path = path + "/" + file

        if file == DATA_FILE:
            continue

        if only_changed:
            last_modified = os.path.getmtime(file_path)

            if last_modified < last_run:
                continue

            if file_path in previous_processed_files and previous_processed_files[file_path] == last_modified:
                continue

        if re.search(regex, file) is not None:
            process_file(file_path)
            current_processed_files[file_path] = os.path.getmtime(file_path)

    if only_changed:
        with open(data_file_path, "w") as f:
            data = {
                'last_run': current_run,
                'processed_files': current_processed_files
            }
            json.dump(data, f)
