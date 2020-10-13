import unittest
import xml.etree.ElementTree as ET

import files2flashcards as f2f
from files2flashcards.formats import cloze

class TestFormatsCloze(unittest.TestCase):

    def test_extract_cloze_data_simple(self):
        """Cloze deletion data should be able to be extracted"""

        raw_string = """<span class="h-fcard e-cloze"><em>This</em></span>"""
        tag = "span"
        fragments = f2f.find_fragments(raw_string, tag)

        root = ET.fromstring(fragments[0])

        data = cloze.extract(root)

        self.assertEqual(data, {"Text": "{{c1::This}}", "Extra": ""})

        raw_string = """<span class="h-fcard e-cloze"><em>That</em></span>"""
        tag = "span"
        fragments = f2f.find_fragments(raw_string, tag)

        root = ET.fromstring(fragments[0])

        data = cloze.extract(root)

        self.assertEqual(data, {"Text": "{{c1::That}}", "Extra": ""})

    def test_extract_cloze_data_advanced(self):
        """Cloze deletion data should be able to be extracted"""

        raw_string = """<span class="h-fcard e-cloze">This <em>is</em> a <em>cloze</em> test</span>"""
        tag = "span"
        fragments = f2f.find_fragments(raw_string, tag)

        root = ET.fromstring(fragments[0])

        data = cloze.extract(root)

        self.assertEqual(data, {"Text": "This {{c1::is}} a {{c2::cloze}} test", "Extra": ""})

    def test_extract_cloze_insert_id(self):
        """Cloze deletions have IDs to ensure stability"""

        raw_string = """<span class="h-fcard e-cloze">This <em>is</em> a <em>cloze</em> test</span>"""
        tag = "span"
        fragments = f2f.find_fragments(raw_string, tag)

        root = ET.fromstring(fragments[0])

        cloze.extract(root)

        self.assertEqual(root[0].attrib['data-id'], "1")
        self.assertEqual(root[1].attrib['data-id'], "2")

    def test_extract_cloze_reuse_id(self):
        """Cloze deletions should reuse the IDs from the fragment"""

        raw_string = """<span class="h-fcard e-cloze">This <em data-id="2">is</em> a <em data-id="1">cloze</em> test</span>"""
        tag = "span"
        fragments = f2f.find_fragments(raw_string, tag)

        root = ET.fromstring(fragments[0])

        data = cloze.extract(root)

        self.assertEqual(data, {"Text": "This {{c2::is}} a {{c1::cloze}} test", "Extra": ""})

    def test_extract_cloze_new_cloze(self):
        """Cloze deletions should handle new deletions in known fragments"""

        raw_string = """<span class="h-fcard e-cloze">A <em data-id="1">B</em> <em>C</em> <em data-id="2">D</em> E <em>F</em></span>"""
        tag = "span"
        fragments = f2f.find_fragments(raw_string, tag)

        root = ET.fromstring(fragments[0])

        data = cloze.extract(root)

        self.assertEqual(data, {"Text": "A {{c1::B}} {{c3::C}} {{c2::D}} E {{c4::F}}", "Extra": ""})
