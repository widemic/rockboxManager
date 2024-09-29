import unittest
from unittest.mock import patch
from rockbox_db_manager.cli import main

class TestCLI(unittest.TestCase):

    @patch("rockbox_db_manager.cli.database.create_rockbox_database")
    def test_create_db_command(self, mock_create_db):
        """Test the create-db command."""
        test_args = ["create-db", "output", "music", "--config", "config.json"]
        with patch("sys.argv", ["main.py"] + test_args):
            main()
        mock_create_db.assert_called_once_with("output", "music", "config.json")

    @patch("rockbox_db_manager.cli.database.validate_database")
    def test_validate_command(self, mock_validate):
        """Test the validate command."""
        test_args = ["validate", "output"]
        with patch("sys.argv", ["main.py"] + test_args):
            main()
        mock_validate.assert_called_once_with("output")

if __name__ == '__main__':
    unittest.main()