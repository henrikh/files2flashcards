import unittest
import xml.etree.ElementTree as ET

import files2flashcards as f2f
from files2flashcards.formats import syntax

class TestFormatsSyntax(unittest.TestCase):

    def test_extract_syntax(self):
        """Programming syntax should be extracted"""

        raw_string = """
<dl class="h-fcard e-programming-syntax"
    data-language="Ada">
    <dt>Addition</dt>
    <dd><pre>2 + 2</pre></dd>
</dl>"""
        tag = "dl"
        fragments = f2f.find_fragments(raw_string, tag)

        root = ET.fromstring(fragments[0])

        data = syntax.extract(root)

        self.assertEqual(data, {"Meaning": "Addition", "Syntax": "2 + 2", "Language": "Ada"})

    def test_extract_syntax_styled(self):
        """Programming syntax should be extracted"""

        raw_string = """
<dl class="h-fcard e-programming-syntax"
    data-language="Ada">
    <dt>Addition</dt>
    <dd><pre>2 <b>+</b> 2</pre></dd>
</dl>"""
        tag = "dl"
        fragments = f2f.find_fragments(raw_string, tag)

        root = ET.fromstring(fragments[0])

        data = syntax.extract(root)

        self.assertEqual(data, {"Meaning": "Addition", "Syntax": "2 <b>+</b> 2", "Language": "Ada"})
