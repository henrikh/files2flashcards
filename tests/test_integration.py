import unittest
import files2flashcards as f2f
import tempfile
import shutil

class TestIntegration(unittest.TestCase):

    def test_new_note(self):
        f2f.AnkiConnectWrapper.deck_name = "Test"
        f2f.AnkiConnectWrapper.invoke("createDeck", {"deck": "Test"})

        f2f.add_format(
            tag="abbr",
            class_name="h-fcard",
            note_type="Basic",
            mapping_function=f2f.extract_abbreviation_basic)

        f2f.add_format(
            tag="span",
            class_name="e-cloze",
            note_type="Cloze",
            mapping_function=f2f.extract_cloze)

        tmp_dir_o = tempfile.TemporaryDirectory()
        tmp_dir = tmp_dir_o.name
        shutil.copyfile("tests/test.tid", tmp_dir + "/" + "test.tid")

        f2f.process_file(tmp_dir + "/" + "test.tid")

        with open(tmp_dir + "/" + "test.tid", "r+", encoding='utf-8') as f:
            content = f.read()

            print(content)

            content = content.replace("BER", "SER")
            content = content.replace("Bit", "Symbol")
            content = content.replace("replace-me", "<em>replace-me</em>")

            f.seek(0)
            f.write(content)
            f.seek(0)
            content = f.read()
            print(content)

        f2f.process_file(tmp_dir + "/" + "test.tid")

        f2f.AnkiConnectWrapper.invoke("deleteDecks", {"decks": ["Test"], "cardsToo": True})