import unittest
import xml.etree.ElementTree as ET

import files2flashcards as f2f
from files2flashcards.formats import synonyms

class TestFormatsSynonyms(unittest.TestCase):

    def test_extract_synonyms_data_simple(self):
        """Synonym lists should be able to be extracted"""

        raw_string = """<ul class="h-fcard e-synonyms">
        <li>This</li>
        <li>That</li>
        </ul>"""

        tag = "ul"
        fragments = f2f.find_fragments(raw_string, tag)

        root = ET.fromstring(fragments[0])

        data = synonyms.extract(root)

        self.assertEqual(data, {"Text": "Synonyms of<br />{{c1::This}}<br />{{c2::That}}", "Extra": ""})

    def test_extract_synonyms_insert_id(self):
        """Synonym lists have IDs to ensure stability"""

        raw_string = """<ul class="h-fcard e-synonyms">
        <li>This</li>
        <li>That</li>
        </ul>"""

        tag = "ul"
        fragments = f2f.find_fragments(raw_string, tag)

        root = ET.fromstring(fragments[0])

        synonyms.extract(root)

        self.assertEqual(root[0].attrib['data-id'], "1")
        self.assertEqual(root[1].attrib['data-id'], "2")

    def test_extract_synonyms_reuse_id(self):
        """Synonym lists should reuse the IDs from the fragment"""

        raw_string = """<ul class="h-fcard e-synonyms">
        <li data-id="2">This</li>
        <li data-id="1">That</li>
        </ul>"""

        tag = "ul"
        fragments = f2f.find_fragments(raw_string, tag)

        root = ET.fromstring(fragments[0])

        data = synonyms.extract(root)

        self.assertEqual(data, {"Text": "Synonyms of<br />{{c2::This}}<br />{{c1::That}}", "Extra": ""})

    def test_extract_synonyms_new_synonym(self):
        """Synonym lists should handle new synonyms in known fragments"""

        raw_string = """<ul class="h-fcard e-synonyms">
        <li>Those</li>
        <li data-id="2">This</li>
        <li data-id="1">That</li>
        </ul>"""

        tag = "ul"
        fragments = f2f.find_fragments(raw_string, tag)

        root = ET.fromstring(fragments[0])

        synonyms.extract(root)

        self.assertEqual(root[0].attrib['data-id'], "3")
