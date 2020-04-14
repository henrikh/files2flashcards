import unittest
import files2flashcards as f2f
import xml.etree.ElementTree as ET

class TestExtractFlashcardData(unittest.TestCase):

    def test_fragments(self):

        raw_string = """<abbr title="Bit error rate" data-context="Communication" class="h-fcard">BER</abbr>"""
        tag = "abbr"
        fragments = f2f.find_fragments(raw_string, tag)

        self.assertEquals(fragments, ["""<abbr title="Bit error rate" data-context="Communication" class="h-fcard">BER</abbr>"""])

        raw_string = """It is <abbr title="Bit error rate" data-context="Communication" class="h-fcard">BER</abbr>"""
        tag = "abbr"
        fragments = f2f.find_fragments(raw_string, tag)

        self.assertEquals(fragments, ["""<abbr title="Bit error rate" data-context="Communication" class="h-fcard">BER</abbr>"""])

    def test_fragments_multiple(self):
        """Ensure that multiple fragments can be extracted from a single file"""

        raw_string = """<abbr title="Bit error rate" data-context="Communication" class="h-fcard">BER</abbr> and another <abbr title="Symbol error rate" data-context="Communication" class="h-fcard">SER</abbr>"""
        tag = "abbr"
        fragments = f2f.find_fragments(raw_string, tag)

        self.assertEquals(fragments, ["""<abbr title="Bit error rate" data-context="Communication" class="h-fcard">BER</abbr>""", """<abbr title="Symbol error rate" data-context="Communication" class="h-fcard">SER</abbr>"""])

    def test_fragments_spanning_lines(self):
        """Ensure that fragments can span multiple lines"""

        raw_string = """
<dl class="h-fcard e-programming-syntax"
    data-language="Ada">
    <dt>Addition</dt>
    <dd><pre>2 + 2</pre></dd>
</dl>"""
        tag = "dl"
        fragments = f2f.find_fragments(raw_string, tag)

        self.assertEquals(fragments, ["""<dl class="h-fcard e-programming-syntax"
    data-language="Ada">
    <dt>Addition</dt>
    <dd><pre>2 + 2</pre></dd>
</dl>"""])

    def test_extract_abbreviation(self):
        """Abbreviations should be able to be extracted"""

        raw_string = """<abbr title="Bit error rate" data-context="Communication" class="h-fcard">BER</abbr>"""
        tag = "abbr"
        fragments = f2f.find_fragments(raw_string, tag)

        root = ET.fromstring(fragments[0])

        data = f2f.extract_abbreviation(root)

        self.assertEquals(data, {"full": "Bit error rate", "context": "Communication", "abbreviation": "BER"})

        raw_string = """<abbr title="Symbol error rate" data-context="Communication" class="h-fcard">SER</abbr>"""
        tag = "abbr"
        fragments = f2f.find_fragments(raw_string, tag)

        root = ET.fromstring(fragments[0])

        data = f2f.extract_abbreviation(root)

        self.assertEquals(data, {"full": "Symbol error rate", "context": "Communication", "abbreviation": "SER"})

    def test_inject_Anki_ID(self):
        """Ability to inject Anki ID in elements"""

        raw_string = """<abbr title="Bit error rate" data-context="Communication" class="h-fcard">BER</abbr>"""
        tag = "abbr"
        fragments = f2f.find_fragments(raw_string, tag)

        root = ET.fromstring(fragments[0])

        root = f2f.inject_Anki_ID(root, 1234)

        fragment = ET.tostring(root, encoding="unicode")

        root = ET.fromstring(fragment)

        self.assertEquals(root.attrib["data-anki-id"], "1234")

        fragments = f2f.find_fragments(fragment, tag)

        root = ET.fromstring(fragments[0])

        data = f2f.extract_abbreviation(root)

        self.assertEquals(data, {"full": "Bit error rate", "context": "Communication", "abbreviation": "BER"})

if __name__ == '__main__':
    unittest.main()