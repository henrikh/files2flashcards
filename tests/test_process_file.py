import unittest
import files2flashcards as f2f
import tempfile
import shutil
import xml.etree.ElementTree as ET
from unittest.mock import MagicMock, Mock, call

class TestProcessFile(unittest.TestCase):

    def test_process_file(self):
        """Register formats and process a file"""

        f2f.add_format(
            tag="abbr",
            class_name="e-abbr",
            note_type="abbreviation",
            mapping_function=f2f.extract_abbreviation)

        tmp_dir = tempfile.gettempdir()
        shutil.copyfile("tests/test.tid", tmp_dir + "/" + "test.tid")

        f2f.process_file(tmp_dir + "/" + "test.tid")

        with open(tmp_dir + "/" + "test.tid") as f:
            content = f.read()

            fragments = f2f.find_fragments(content, "abbr")

            root = ET.fromstring(fragments[0])

            data = f2f.extract_abbreviation(root)

            self.assertEquals(data, {"full": "Bit error rate", "context": "Communication", "abbreviation": "BER"})

            print(content)

    def test_process_file_no_flashcards(self):
        """There can be things which looks like flashcards, but aren't
        
        Here we check that when the e-abbr class is not present, then flashcards shouldn't be processed"""

        f2f.add_format(
            tag="abbr",
            class_name="e-abbr",
            note_type="abbreviation",
            mapping_function=f2f.extract_abbreviation)

        tmp_dir = tempfile.gettempdir()
        shutil.copyfile("tests/test_no_flashcard.tid", tmp_dir + "/" + "test.tid")

        content_before = ""

        with open(tmp_dir + "/" + "test.tid") as f:
            content_before = f.read()

        f2f.process_file(tmp_dir + "/" + "test.tid")

        with open(tmp_dir + "/" + "test.tid") as f:
            content = f.read()

            self.assertEqual(content, content_before)

    def test_process_file_call_Anki(self):
        """Register formats and process a file"""

        f2f.add_format(
            tag="abbr",
            class_name="e-abbr",
            note_type="abbreviation",
            mapping_function=f2f.extract_abbreviation)

        tmp_dir = tempfile.gettempdir()
        shutil.copyfile("tests/test.tid", tmp_dir + "/" + "test.tid")

        f2f.AnkiConnectWrapper.add_note = MagicMock()
        f2f.AnkiConnectWrapper.add_note.return_value = "123456"

        f2f.process_file(tmp_dir + "/" + "test.tid")

        f2f.AnkiConnectWrapper.add_note.assert_called_with("abbreviation", {"full": "Bit error rate", "context": "Communication", "abbreviation":"BER"})

        with open(tmp_dir + "/" + "test.tid") as f:
            content = f.read()

            self.assertIn("123456", content)

if __name__ == '__main__':
    unittest.main()