import unittest
from files2flashcards import AnkiConnectWrapper as acw
from unittest.mock import MagicMock, Mock, call

class TestAnkiConnectWrapper(unittest.TestCase):

    def test_add_note(self):
        """Calling convention for adding note"""

        acw.invoke = MagicMock()

        acw.invoke.return_value = "12345"

        id = acw.add_note("Basic", {"Front": "front content", "Back": "back content"})

        self.assertEqual(id, "12345")

        acw.invoke.assert_called_with("addNote",
            {"note":
                {"deckName": "Default",
                "modelName": "Basic",
                "fields": {"Front": "front content", "Back": "back content"},
                "options": {
                    "allowDuplicates": False
                    },
                "tags": []
            }})

    def test_update_note(self):
        """Calling convention for adding note"""

        acw.invoke = MagicMock()

        acw.update_note("12345", {"Front": "front content", "Back": "back content"})

        acw.invoke.assert_called_with("updateNoteFields",
            {"note": {"id": "12345",
            "fields": {"Front": "front content", "Back": "back content"}}})

if __name__ == '__main__':
    unittest.main()
