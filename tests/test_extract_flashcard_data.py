import unittest
import files2flashcards as f2f

class TestExtractFlashcardData(unittest.TestCase):

    def test_fragments(self):

        raw_string = """<abbr title="Bit error rate" data-context="Communication">BER</abbr>"""
        tag = "abbr"
        fragments = f2f.find_fragments(raw_string, tag)

        self.assertEquals(fragments, ["""<abbr title="Bit error rate" data-context="Communication">BER</abbr>"""])

        raw_string = """It is <abbr title="Bit error rate" data-context="Communication">BER</abbr>"""
        tag = "abbr"
        fragments = f2f.find_fragments(raw_string, tag)

        self.assertEquals(fragments, ["""<abbr title="Bit error rate" data-context="Communication">BER</abbr>"""])

    def test_fragments_multiple(self):
        """Ensure that multiple fragments can be extracted from a single file"""

        raw_string = """<abbr title="Bit error rate" data-context="Communication">BER</abbr> and another <abbr title="Symbol error rate" data-context="Communication">SER</abbr>"""
        tag = "abbr"
        fragments = f2f.find_fragments(raw_string, tag)

        self.assertEquals(fragments, ["""<abbr title="Bit error rate" data-context="Communication">BER</abbr>""", """<abbr title="Symbol error rate" data-context="Communication">SER</abbr>"""])

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

if __name__ == '__main__':
    unittest.main()