import unittest
import xml.etree.ElementTree as ET
import tempfile
import shutil
import os
from unittest.mock import MagicMock, Mock, call

import files2flashcards as f2f
from files2flashcards.formats import abbreviation

class TestExtractFlashcardData(unittest.TestCase):

    def test_fragments(self):

        raw_string = """<abbr title="Bit error rate" data-context="Communication" class="h-fcard">BER</abbr>"""
        tag = "abbr"
        fragments = f2f.find_fragments(raw_string, tag)

        self.assertEqual(fragments, ["""<abbr title="Bit error rate" data-context="Communication" class="h-fcard">BER</abbr>"""])

        raw_string = """It is <abbr title="Bit error rate" data-context="Communication" class="h-fcard">BER</abbr>"""
        tag = "abbr"
        fragments = f2f.find_fragments(raw_string, tag)

        self.assertEqual(fragments, ["""<abbr title="Bit error rate" data-context="Communication" class="h-fcard">BER</abbr>"""])

    def test_fragments_multiple(self):
        """Ensure that multiple fragments can be extracted from a single file"""

        raw_string = """<abbr title="Bit error rate" data-context="Communication" class="h-fcard">BER</abbr> and another <abbr title="Symbol error rate" data-context="Communication" class="h-fcard">SER</abbr>"""
        tag = "abbr"
        fragments = f2f.find_fragments(raw_string, tag)

        self.assertEqual(fragments, ["""<abbr title="Bit error rate" data-context="Communication" class="h-fcard">BER</abbr>""", """<abbr title="Symbol error rate" data-context="Communication" class="h-fcard">SER</abbr>"""])

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

        self.assertEqual(fragments, ["""<dl class="h-fcard e-programming-syntax"
    data-language="Ada">
    <dt>Addition</dt>
    <dd><pre>2 + 2</pre></dd>
</dl>"""])

    def test_inject_Anki_ID(self):
        """Ability to inject Anki ID in elements"""

        raw_string = """<abbr title="Bit error rate" data-context="Communication" class="h-fcard">BER</abbr>"""
        tag = "abbr"
        fragments = f2f.find_fragments(raw_string, tag)

        root = ET.fromstring(fragments[0])

        root = f2f.inject_Anki_ID(root, 1234)

        fragment = ET.tostring(root, encoding="unicode")

        root = ET.fromstring(fragment)

        self.assertEqual(root.attrib["data-anki-id"], "1234")

        fragments = f2f.find_fragments(fragment, tag)

        root = ET.fromstring(fragments[0])

        data = f2f.extract_abbreviation_basic(root)

        self.assertEqual(data, {"Back": "Bit error rate", "Front": "BER"})

class TestProcessFile(unittest.TestCase):

    def setUp(self):
        f2f.AnkiConnectWrapper.add_note = MagicMock()
        f2f.AnkiConnectWrapper.add_note.return_value = "1234"
        f2f.AnkiConnectWrapper.update_note = MagicMock()

    def test_process_file(self):
        """Register formats and process a file"""

        f2f.AnkiConnectWrapper.add_note = MagicMock()
        f2f.AnkiConnectWrapper.add_note.return_value = "1234"
        f2f.AnkiConnectWrapper.update_note = MagicMock()

        f2f.add_format(**abbreviation.definition)

        tmp_dir_o = tempfile.TemporaryDirectory()
        tmp_dir = tmp_dir_o.name
        shutil.copyfile("tests/test.tid", tmp_dir + "/" + "test.tid")

        f2f.process_file(tmp_dir + "/" + "test.tid")

        with open(tmp_dir + "/" + "test.tid", encoding='utf-8') as f:
            content = f.read()

            fragments = f2f.find_fragments(content, "abbr")

            root = ET.fromstring(fragments[0])

            data = abbreviation.extract(root)

            self.assertEqual(data, {"Full": "Bit error rate", "Context": "Communication", "Abbreviation": "BER"})

            print(content)

    def test_process_file_return_ElementTree_modified(self):
        """Modify the ElementTree in the mapping function"""

        f2f.AnkiConnectWrapper.add_note = MagicMock()
        f2f.AnkiConnectWrapper.add_note.return_value = "1234"
        f2f.AnkiConnectWrapper.update_note = MagicMock()

        tmp_dir_o = tempfile.TemporaryDirectory()
        tmp_dir = tmp_dir_o.name
        shutil.copyfile("tests/test.tid", tmp_dir + "/" + "test.tid")

        def edit_ElementTree(root):
            root.attrib["data-dummy"] = "test"
            return abbreviation.extract(root)

        f2f.add_format(
            tag="abbr",
            class_name="h-fcard",
            note_type="Abbreviation",
            mapping_function=edit_ElementTree)

        f2f.process_file(tmp_dir + "/" + "test.tid")

        with open(tmp_dir + "/" + "test.tid", encoding='utf-8') as f:
            content = f.read()

            self.assertIn('data-dummy="test"', content)

    def test_process_file_return_ElementTree_modified_existing(self):
        """Modify the ElementTree in the mapping function"""

        f2f.AnkiConnectWrapper.add_note = MagicMock()
        f2f.AnkiConnectWrapper.add_note.return_value = "1234"
        f2f.AnkiConnectWrapper.update_note = MagicMock()

        tmp_dir_o = tempfile.TemporaryDirectory()
        tmp_dir = tmp_dir_o.name
        shutil.copyfile("tests/test_existing_note.tid", tmp_dir + "/" + "test.tid")

        def edit_ElementTree(root):
            root.attrib["data-dummy"] = "test"
            return abbreviation.extract(root)

        f2f.add_format(
            tag="abbr",
            class_name="h-fcard",
            note_type="Abbreviation",
            mapping_function=edit_ElementTree)

        f2f.process_file(tmp_dir + "/" + "test.tid")

        with open(tmp_dir + "/" + "test.tid", encoding='utf-8') as f:
            content = f.read()

            self.assertIn('data-dummy="test"', content)

    def test_process_file_taboo_word(self):
        """Ignore files with the taboo word"""

        f2f.AnkiConnectWrapper.add_note = MagicMock()
        f2f.AnkiConnectWrapper.add_note.return_value = "1234"
        f2f.AnkiConnectWrapper.update_note = MagicMock()

        f2f.taboo_word = "Taboo!"

        f2f.add_format(**abbreviation.definition)

        tmp_dir_o = tempfile.TemporaryDirectory()
        tmp_dir = tmp_dir_o.name
        shutil.copyfile("tests/test_taboo.tid", tmp_dir + "/" + "test.tid")

        content_before = ""

        with open(tmp_dir + "/" + "test.tid", encoding='utf-8') as f:
            content_before = f.read()

        f2f.process_file(tmp_dir + "/" + "test.tid")

        with open(tmp_dir + "/" + "test.tid", encoding='utf-8') as f:
            self.assertEqual(content_before, f.read())

    def test_process_file_no_flashcards(self):
        """There can be things which looks like flashcards, but aren't
        
        Here we check that when the h-fcard class is not present, then flashcards shouldn't be processed"""

        f2f.add_format(**abbreviation.definition)

        tmp_dir_o = tempfile.TemporaryDirectory()
        tmp_dir = tmp_dir_o.name
        shutil.copyfile("tests/test_no_flashcard.tid", tmp_dir + "/" + "test.tid")

        content_before = ""

        with open(tmp_dir + "/" + "test.tid", encoding='utf-8') as f:
            content_before = f.read()

        f2f.process_file(tmp_dir + "/" + "test.tid")

        with open(tmp_dir + "/" + "test.tid", encoding='utf-8') as f:
            content = f.read()

            self.assertEqual(content, content_before)

    def test_process_file_call_Anki(self):
        """New notes should be requested to be added"""

        f2f.add_format(**abbreviation.definition)

        tmp_dir_o = tempfile.TemporaryDirectory()
        tmp_dir = tmp_dir_o.name
        shutil.copyfile("tests/test.tid", tmp_dir + "/" + "test.tid")

        f2f.AnkiConnectWrapper.add_note = MagicMock()
        f2f.AnkiConnectWrapper.add_note.return_value = "123456"

        f2f.process_file(tmp_dir + "/" + "test.tid")

        f2f.AnkiConnectWrapper.add_note.assert_called_with("Abbreviation", {"Full": "Bit error rate", "Context": "Communication", "Abbreviation":"BER"})

        with open(tmp_dir + "/" + "test.tid", encoding='utf-8') as f:
            content = f.read()

            self.assertIn("123456", content)

    def test_process_file_call_Anki_existing_note(self):
        """Existing notes should be requested to be updated"""

        f2f.add_format(**abbreviation.definition)

        tmp_dir_o = tempfile.TemporaryDirectory()
        tmp_dir = tmp_dir_o.name
        shutil.copyfile("tests/test_existing_note.tid", tmp_dir + "/" + "test.tid")

        f2f.AnkiConnectWrapper.update_note = MagicMock()

        f2f.process_file(tmp_dir + "/" + "test.tid")

        f2f.AnkiConnectWrapper.update_note.assert_called_with("654321", {"Full": "Bit error rate", "Context": "Communication", "Abbreviation":"BER"})

    def test_process_folder(self):
        """Process a whole folder of notes"""

        f2f.add_format(**abbreviation.definition)

        tmp_dir_o = tempfile.TemporaryDirectory()
        tmp_dir = tmp_dir_o.name

        shutil.copyfile("tests/test.tid", tmp_dir + "/" + "test1.tid")
        shutil.copyfile("tests/test.tid", tmp_dir + "/" + "test2.tid")

        f2f.process_file = MagicMock()

        f2f.process_folder(tmp_dir)

        self.assertEqual(f2f.process_file.call_count, 2)

    def test_process_folder_regex(self):
        """Use a regex to limit which files are processed"""

        f2f.add_format(**abbreviation.definition)

        tmp_dir_o = tempfile.TemporaryDirectory()
        tmp_dir = tmp_dir_o.name

        shutil.copyfile("tests/test.tid", tmp_dir + "/" + "test1.tid")
        shutil.copyfile("tests/test.tid", tmp_dir + "/" + "test2.md")

        f2f.process_file = MagicMock()

        f2f.process_folder(tmp_dir, regex=r'\.tid$')

        self.assertEqual(f2f.process_file.call_count, 1)

    def test_process_folder_changed(self):
        """Only process files if they have changed"""

        f2f.add_format(**abbreviation.definition)

        tmp_dir_o = tempfile.TemporaryDirectory()
        tmp_dir = tmp_dir_o.name

        shutil.copyfile("tests/test.tid", tmp_dir + "/" + "test1.tid")

        f2f.AnkiConnectWrapper.add_note = Mock()
        f2f.AnkiConnectWrapper.add_note.return_value = "12345"
        f2f.AnkiConnectWrapper.update_note = Mock()

        f2f.process_folder(tmp_dir, only_changed=True)

        self.assertEqual(f2f.AnkiConnectWrapper.add_note.call_count, 1)

        f2f.AnkiConnectWrapper.add_note.reset_mock()

        shutil.copyfile("tests/test.tid", tmp_dir + "/" + "test2.tid")

        f2f.process_folder(tmp_dir, only_changed=True)

        self.assertEqual(f2f.AnkiConnectWrapper.add_note.call_count, 1)
        self.assertEqual(f2f.AnkiConnectWrapper.update_note.call_count, 0)

    def test_process_folder_changed_custom_folder(self):
        """Select a different folder for the data file"""

        f2f.add_format(**abbreviation.definition)

        tmp_dir_o = tempfile.TemporaryDirectory()
        tmp_dir = tmp_dir_o.name

        tmp_data_dir_o = tempfile.TemporaryDirectory()
        tmp_data_dir = tmp_data_dir_o.name

        shutil.copyfile("tests/test.tid", tmp_dir + "/" + "test1.tid")

        f2f.AnkiConnectWrapper.add_note = Mock()
        f2f.AnkiConnectWrapper.add_note.return_value = "12345"
        f2f.AnkiConnectWrapper.update_note = Mock()

        f2f.process_folder(tmp_dir, only_changed=True, data_file_dir=tmp_data_dir)

        f2f.AnkiConnectWrapper.add_note.reset_mock()

        shutil.copyfile("tests/test.tid", tmp_dir + "/" + "test2.tid")

        f2f.process_folder(tmp_dir, only_changed=True, data_file_dir=tmp_data_dir)

        self.assertEqual(f2f.AnkiConnectWrapper.add_note.call_count, 1)
        self.assertEqual(f2f.AnkiConnectWrapper.update_note.call_count, 0)

if __name__ == '__main__':
    unittest.main()
