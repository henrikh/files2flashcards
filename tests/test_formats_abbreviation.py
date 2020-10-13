import unittest
import xml.etree.ElementTree as ET

import files2flashcards as f2f
from files2flashcards.formats import abbreviation

class TestFormatsAbbreviation(unittest.TestCase):

    def test_extract_abbreviation(self):
        """Abbreviations should be able to be extracted"""

        raw_string = """<abbr title="Bit error rate" data-context="Communication" class="h-fcard">BER</abbr>"""
        tag = "abbr"
        fragments = f2f.find_fragments(raw_string, tag)

        root = ET.fromstring(fragments[0])

        data = abbreviation.extract(root)

        self.assertEqual(data, {"Full": "Bit error rate", "Context": "Communication", "Abbreviation": "BER"})

        raw_string = """<abbr title="Symbol error rate" data-context="Communication" class="h-fcard">SER</abbr>"""
        tag = "abbr"
        fragments = f2f.find_fragments(raw_string, tag)

        root = ET.fromstring(fragments[0])

        data = abbreviation.extract(root)

        self.assertEqual(data, {"Full": "Symbol error rate", "Context": "Communication", "Abbreviation": "SER"})
