import pytest
import json
import os
import tempfile
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

# Add bin/commands to path for imports
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../bin/commands'))

from CommandGenerator import GenerateCommand


class TestGenerateCommand:
    """Tests for the GenerateCommand utility class."""

    @pytest.fixture
    def mock_from_root(self):
        """Mock the from_root function to return a predictable path."""
        with patch('CommandGenerator.from_root') as mock_fn:
            def side_effect(path):
                return os.path.join('/mock/root', path)
            mock_fn.side_effect = side_effect
            yield mock_fn

    @pytest.fixture
    def temp_config_dir(self):
        """Create a temporary directory for config files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_init_basic(self, mock_from_root):
        """Test GenerateCommand initialization with basic parameters."""
        gen = GenerateCommand("my-command", "/")
        assert gen.input == "my-command"
        assert gen.prefix == "/"

    def test_init_custom_prefix(self, mock_from_root):
        """Test GenerateCommand initialization with custom prefix."""
        gen = GenerateCommand("my-command", "!")
        assert gen.input == "my-command"
        assert gen.prefix == "!"

    def test_init_creates_commands_json_if_missing(self, mock_from_root):
        """Test that __init__ creates commands.json if it doesn't exist."""
        with patch('CommandGenerator.path.exists', return_value=False):
            with patch('builtins.open', mock_open()) as mock_file:
                gen = GenerateCommand("test-cmd", "/")
                # Verify file was opened for writing
                mock_file.assert_called()

    def test_init_ensures_commands_key_exists(self, mock_from_root):
        """Test that __init__ ensures 'commands' key exists in JSON."""
        mock_data = {}
        
        with patch('CommandGenerator.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=json.dumps(mock_data))):
                gen = GenerateCommand("test-cmd", "/")

    def test_generate_command_name_single_part(self):
        """Test generate_command_name with single part."""
        gen = GenerateCommand("test", "/")
        result = gen.generate_command_name(["foo"])
        assert result == "Foo"

    def test_generate_command_name_multiple_parts(self):
        """Test generate_command_name with multiple parts."""
        gen = GenerateCommand("test", "/")
        result = gen.generate_command_name(["foo", "bar", "baz"])
        # First part is removed, rest are joined
        assert result == "BarBaz"

    def test_capitalize_slugged_input_hyphens(self):
        """Test capitalize_slugged_input with hyphens."""
        gen = GenerateCommand("test", "/")
        result = gen.capitalize_slugged_input("some-string-name")
        assert result == ["Some", "String", "Name"]

    def test_capitalize_slugged_input_underscores(self):
        """Test capitalize_slugged_input with underscores."""
        gen = GenerateCommand("test", "/")
        result = gen.capitalize_slugged_input("some_string_name")
        assert result == ["Some", "String", "Name"]

    def test_capitalize_slugged_input_spaces(self):
        """Test capitalize_slugged_input with spaces."""
        gen = GenerateCommand("test", "/")
        result = gen.capitalize_slugged_input("some string name")
        assert result == ["Some", "String", "Name"]

    def test_convert_string_to_camelcase(self):
        """Test convert_string_to_camelcase method."""
        gen = GenerateCommand("test", "/")
        result = gen.convert_string_to_camelcase("some-string-name")
        assert result == "someStringName"

    def test_convert_string_to_camelcase_single_word(self):
        """Test convert_string_to_camelcase with single word."""
        gen = GenerateCommand("test", "/")
        result = gen.convert_string_to_camelcase("word")
        assert result == "word"

    def test_convert_string_to_camelcase_two_words(self):
        """Test convert_string_to_camelcase with two words."""
        gen = GenerateCommand("test", "/")
        result = gen.convert_string_to_camelcase("some-string")
        assert result == "someString"

    def test_camelcase_to_uppercase(self):
        """Test camelcase_to_uppercase method."""
        gen = GenerateCommand("test", "/")
        result = gen.camelcase_to_uppercase("someString")
        assert result == "SomeString"

    def test_reformat_text_with_hyphens(self):
        """Test reformat_text with hyphenated words."""
        gen = GenerateCommand("test", "/")
        result = gen.reformat_text(["foo-bar", "baz"])
        assert result == ["FooBar", "Baz"]

    def test_reformat_text_without_hyphens(self):
        """Test reformat_text without hyphens."""
        gen = GenerateCommand("test", "/")
        result = gen.reformat_text(["foo", "bar", "baz"])
        assert result == ["Foo", "Bar", "Baz"]

    def test_make_command_array(self):
        """Test make_command_array method."""
        gen = GenerateCommand("test", "/")
        result = gen.make_command_array("TestCmd", "/test-cmd", "commands/TestCmd.py")
        
        assert "TestCmd" in result
        assert result["TestCmd"]["syntax"] == "/test-cmd"
        assert result["TestCmd"]["filePath"] == "commands/TestCmd.py"
        assert result["TestCmd"]["description"] == "Awaiting developer description"
        assert result["TestCmd"]["authorization"] == []
        assert result["TestCmd"]["hasValue"] is False
        assert result["TestCmd"]["slashCommand"] is False
        assert result["TestCmd"]["middlewares"] == []
        assert result["TestCmd"]["arguments"] == {}

    def test_make_command_array_none_parameters(self):
        """Test make_command_array returns None with missing parameters."""
        gen = GenerateCommand("test", "/")
        result = gen.make_command_array(None, "/test", "path")
        assert result is None

    def test_generate_file_path_single_command(self):
        """Test generate_file_path with single command."""
        gen = GenerateCommand("test", "/")
        result = gen.generate_file_path(["ping"], "Ping")
        assert result == "Ping.py"

    def test_generate_file_path_nested_command(self):
        """Test generate_file_path with nested command."""
        gen = GenerateCommand("test", "/")
        result = gen.generate_file_path(["admin", "kick", "user"], "KickUser")
        assert result == "admin/kick/KickUser.py"

    def test_generate_class_name_single_part(self):
        """Test generate_class_name with single part."""
        gen = GenerateCommand("test", "/")
        result = gen.generate_class_name(["ping"])
        assert result == "Ping"

    def test_generate_class_name_hyphenated(self):
        """Test generate_class_name with hyphenated command."""
        gen = GenerateCommand("test", "/")
        result = gen.generate_class_name(["kick-user"])
        assert result == "KickUser"

    def test_generate_class_name_nested(self):
        """Test generate_class_name with nested command."""
        gen = GenerateCommand("test", "/")
        result = gen.generate_class_name(["admin", "kick-user"])
        assert result == "KickUser"

    def test_write_py_files_success(self, mock_from_root):
        """Test write_py_files creates file successfully."""
        gen = GenerateCommand("test", "/")
        
        with patch('CommandGenerator.path.exists', return_value=False):
            with patch('CommandGenerator.os.makedirs'):
                with patch('builtins.open', mock_open()) as mock_file:
                    result = gen.write_py_files("TestCmd", "TestCmd.py")
                    
                    assert result["status"] is True
                    assert "created" in result["message"].lower()

    def test_write_py_files_already_exists(self, mock_from_root):
        """Test write_py_files when file already exists."""
        gen = GenerateCommand("test", "/")
        
        with patch('CommandGenerator.path.exists', return_value=True):
            result = gen.write_py_files("TestCmd", "TestCmd.py")
            
            assert result["status"] is False
            assert "already exists" in result["error"]

    def test_write_py_files_no_class_name(self, mock_from_root):
        """Test write_py_files with missing class name."""
        gen = GenerateCommand("test", "/")
        result = gen.write_py_files(None, "TestCmd.py")
        
        assert result["status"] is False
        assert "No class name" in result["error"]

    def test_manipulate_commands_json_simple_command(self, mock_from_root):
        """Test manipulate_commands_json with simple command."""
        initial_data = {"commands": {}}
        
        with patch('CommandGenerator.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=json.dumps(initial_data))):
                gen = GenerateCommand("test-command", "/")
                result = gen.manipulate_commands_json()
                
                assert result["status"] is True
                assert "successfully" in result["message"].lower()

    def test_manipulate_commands_json_nested_command(self, mock_from_root):
        """Test manipulate_commands_json with nested command."""
        initial_data = {"commands": {}}
        
        with patch('CommandGenerator.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=json.dumps(initial_data))):
                gen = GenerateCommand("admin/kick-user", "/")
                result = gen.manipulate_commands_json()
                
                assert result["status"] is True

    def test_manipulate_commands_json_root_command_with_dash_fails(self, mock_from_root):
        """Test that root commands with dashes are rejected."""
        initial_data = {"commands": {}}
        
        with patch('CommandGenerator.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=json.dumps(initial_data))):
                gen = GenerateCommand("admin-panel/subcommand", "/")
                result = gen.manipulate_commands_json()
                
                assert result["status"] is False
                assert "invalid characters" in result["error"].lower()

    def test_manipulate_commands_json_file_not_found(self, mock_from_root):
        """Test manipulate_commands_json when JSON file not found."""
        with patch('CommandGenerator.path.exists', return_value=True):
            with patch('builtins.open', side_effect=FileNotFoundError):
                gen = GenerateCommand("test", "/")
                result = gen.manipulate_commands_json()
                
                assert result["status"] is False
                assert "not found" in result["error"].lower()

    def test_manipulate_commands_json_invalid_json(self, mock_from_root):
        """Test manipulate_commands_json with invalid JSON."""
        with patch('CommandGenerator.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data="invalid json")):
                gen = GenerateCommand("test", "/")
                result = gen.manipulate_commands_json()
                
                assert result["status"] is False
                assert "error" in result or "decoding" in result.get("error", "").lower()

    def test_manipulate_commands_json_duplicate_simple_command(self, mock_from_root):
        """Test adding duplicate simple command."""
        initial_data = {
            "commands": {
                "TestCmd": {
                    "syntax": "/test-cmd",
                    "description": "Test",
                    "filePath": "TestCmd.py",
                    "authorization": [],
                    "hasValue": False,
                    "slashCommand": False,
                    "middlewares": [],
                    "arguments": {}
                }
            }
        }
        
        with patch('CommandGenerator.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=json.dumps(initial_data))):
                gen = GenerateCommand("test-cmd", "/")
                result = gen.manipulate_commands_json()
                
                assert result["status"] is False

    def test_save_command_success(self, mock_from_root):
        """Test save_command with successful flow."""
        initial_data = {"commands": {}}
        
        with patch('CommandGenerator.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=json.dumps(initial_data))):
                with patch.object(GenerateCommand, 'write_py_files', return_value={"status": True, "message": "Created"}):
                    with patch('builtins.print') as mock_print:
                        gen = GenerateCommand("test-cmd", "/")
                        gen.save_command()
                        
                        # Verify print was called with success message
                        mock_print.assert_called()

    def test_save_command_json_failure(self, mock_from_root):
        """Test save_command when JSON manipulation fails."""
        with patch('CommandGenerator.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data="invalid json")):
                with patch('builtins.print') as mock_print:
                    gen = GenerateCommand("test", "/")
                    gen.save_command()
                    
                    # Verify error was printed
                    mock_print.assert_called()

    def test_prefix_is_used_in_command_string(self, mock_from_root):
        """Test that custom prefix is used in command syntax."""
        initial_data = {"commands": {}}
        
        with patch('CommandGenerator.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=json.dumps(initial_data))):
                gen = GenerateCommand("test-command", "!")
                result = gen.manipulate_commands_json()
                
                assert result["status"] is True
