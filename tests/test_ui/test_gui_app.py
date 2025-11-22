import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Mock tkinter before importing gui_app
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()
sys.modules['tkinter.scrolledtext'] = MagicMock()

from devkit_zero.ui.gui_app import DevKitZeroGUI

class TestDevKitZeroGUI(unittest.TestCase):
    def setUp(self):
        # Patch the root creation to avoid actual window spawning
        with patch('devkit_zero.ui.gui_app.tk.Tk'):
            self.app = DevKitZeroGUI()
            # Mock the internal widgets that are created during setup
            self.app.result_text = MagicMock()
            self.app.control_container = MagicMock()
            self.app.result_container = MagicMock()
            self.app.format_code_text = MagicMock()
            self.app.format_lang_var = MagicMock()
            self.app.format_input_type = MagicMock()

    def test_initialization(self):
        """Test that the GUI initializes correctly"""
        self.assertIsNotNone(self.app)
        self.assertIsNotNone(self.app.tool_var)

    @patch('devkit_zero.ui.gui_app.formatter')
    def test_run_formatter_direct_input(self, mock_formatter):
        """Test running formatter with direct text input"""
        # Setup mocks
        self.app.format_lang_var.get.return_value = "python"
        self.app.format_input_type.get.return_value = "text"
        self.app.format_code_text.get.return_value = "def foo(): pass"
        mock_formatter.format_code.return_value = "formatted code"

        # Run method
        self.app.run_formatter()

        # Verify calls
        mock_formatter.format_code.assert_called_with("def foo(): pass", "python")
        self.app.result_text.delete.assert_called()
        self.app.result_text.insert.assert_called_with(1.0, "formatted code")

    @patch('devkit_zero.ui.gui_app.random_gen')
    def test_run_random_gen_uuid(self, mock_random_gen):
        """Test random generator for UUID"""
        # Setup mocks
        self.app.random_type_var = MagicMock()
        self.app.random_type_var.get.return_value = "uuid"
        mock_random_gen.generate_uuid.return_value = "fake-uuid"

        # Run method
        self.app.run_random_gen()

        # Verify calls
        mock_random_gen.generate_uuid.assert_called_once()
        self.app.result_text.insert.assert_called_with(1.0, "fake-uuid")

    @patch('devkit_zero.ui.gui_app.converter')
    def test_run_converter_json_to_csv(self, mock_converter):
        """Test converter tool"""
        # Setup mocks
        self.app.convert_from_var = MagicMock()
        self.app.convert_to_var = MagicMock()
        self.app.convert_input_text = MagicMock()
        
        self.app.convert_from_var.get.return_value = "json"
        self.app.convert_to_var.get.return_value = "csv"
        self.app.convert_input_text.get.return_value = '[{"a": 1}]'
        mock_converter.json_to_csv.return_value = "a\n1"

        # Run method
        self.app.run_converter()

        # Verify calls
        mock_converter.json_to_csv.assert_called_with('[{"a": 1}]')
        self.app.result_text.insert.assert_called_with(1.0, "a\n1")

if __name__ == '__main__':
    unittest.main()
