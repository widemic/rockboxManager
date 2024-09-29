import unittest
from unittest.mock import patch, mock_open
from rockbox_db_manager.database import create_tag_file, clean_metadata

class TestDatabase(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    def test_create_tag_file(self, mock_file):
        """Test that tag files are created properly."""
        tag_data = {"Artist 1", "Artist 2"}
        create_tag_file("test.tcd", tag_data)
        mock_file.assert_called_with("test.tcd", 'wb')

    def test_clean_metadata(self):
        """Test that metadata is cleaned and defaults are applied correctly."""
        self.assertEqual(clean_metadata("   ", "Unknown Artist"), "Unknown Artist")
        self.assertEqual(clean_metadata("Valid Artist", "Unknown Artist"), "Valid Artist")

if __name__ == '__main__':
    unittest.main()