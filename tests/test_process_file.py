import unittest
import files2flashcards as f2f
import tempfile
import shutil
import xml.etree.ElementTree as ET

class TestProcessFile(unittest.TestCase):

    def test_process_file(self):
        """Register formats and process a file"""

        f2f.add_format("abbr", "e-abbr", f2f.extract_abbreviation)

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

if __name__ == '__main__':
    unittest.main()