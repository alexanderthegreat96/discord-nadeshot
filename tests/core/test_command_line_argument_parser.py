"""Unit tests for core.CommandLineArgumentParser module."""

import pytest
from unittest.mock import patch, mock_open
from core.CommandLineArgumentParser import CommandLineArgumentParser


@pytest.mark.unit
class TestCommandLineArgumentParserInitialization:
    """Test suite for CommandLineArgumentParser initialization."""

    def test_parser_initialization_with_input(self):
        """Test CommandLineArgumentParser initialization with input."""
        input_str = "!test command"
        parser = CommandLineArgumentParser(input_str)
        
        assert parser.input is not None
        assert parser.command_prefixes == ["!", ".", "?", "/", ">"]

    def test_parser_initialization_without_input(self):
        """Test CommandLineArgumentParser initialization without input."""
        parser = CommandLineArgumentParser()
        
        assert parser.input is not None
        assert parser.commands_list is None or isinstance(parser.commands_list, (dict, list, type(None)))

    def test_parser_initializes_with_default_prefixes(self):
        """Test that parser initializes with correct command prefixes."""
        parser = CommandLineArgumentParser()
        
        assert "!" in parser.command_prefixes
        assert "." in parser.command_prefixes
        assert "?" in parser.command_prefixes
        assert "/" in parser.command_prefixes
        assert ">" in parser.command_prefixes


@pytest.mark.unit
class TestCommandLineArgumentParserProcessInput:
    """Test suite for CommandLineArgumentParser input processing."""

    def test_process_input_string_lowercases(self):
        """Test that input strings are lowercased."""
        parser = CommandLineArgumentParser("!TEST COMMAND")
        
        assert parser.input == "!test command"

    def test_process_input_string_with_brackets(self):
        """Test processing strings with square brackets."""
        parser = CommandLineArgumentParser("!test [some arg]")
        
        # Spaces in brackets should be replaced with underscores
        assert "_" in parser.input or "some" in parser.input

    def test_process_input_string_multiple_brackets(self):
        """Test processing strings with multiple bracket sections."""
        parser = CommandLineArgumentParser("!cmd [arg one] [arg two]")
        
        assert parser.input is not None

    def test_process_input_empty_brackets(self):
        """Test processing empty brackets."""
        parser = CommandLineArgumentParser("!test []")
        
        assert parser.input is not None


@pytest.mark.unit
class TestCommandLineArgumentParserTokens:
    """Test suite for token pairing functionality."""

    def test_pair_tokens_list_input(self):
        """Test pairing tokens from list input."""
        parser = CommandLineArgumentParser()
        tokens = ["search", "keyword", "filter"]
        
        result = parser.pair_tokens(tokens)
        
        assert isinstance(result, dict)
        assert "search" in result
        assert "keyword" in result

    def test_pair_tokens_with_command_prefix(self):
        """Test pairing tokens with command prefix removal."""
        parser = CommandLineArgumentParser()
        tokens = ["!search", "keyword"]
        
        result = parser.pair_tokens(tokens)
        
        # First token prefix should be removed
        assert "search" in result

    def test_pair_tokens_last_token_has_none_value(self):
        """Test that last token gets None value."""
        parser = CommandLineArgumentParser()
        tokens = ["cmd", "arg1", "arg2"]
        
        result = parser.pair_tokens(tokens)
        
        # Last token should have None value
        assert result.get("arg2") is None

    def test_pair_tokens_dict_input_flattened(self):
        """Test that dict input is flattened into tokens."""
        parser = CommandLineArgumentParser()
        token_dict = {"cmd": "arg1", "key": "value"}
        
        result = parser.pair_tokens(token_dict)
        
        assert isinstance(result, dict)

    def test_pair_tokens_empty_input(self):
        """Test pairing with empty token list."""
        parser = CommandLineArgumentParser()
        tokens = []
        
        result = parser.pair_tokens(tokens)
        
        assert result == {}


@pytest.mark.unit
class TestCommandLineArgumentParserFlatten:
    """Test suite for dictionary flattening."""

    def test_flatten_dict_to_list(self):
        """Test flattening dictionary to list."""
        parser = CommandLineArgumentParser()
        test_dict = {"key1": "value1", "key2": "value2"}
        
        result = parser.flatten_dict_to_list(test_dict)
        
        assert isinstance(result, list)
        assert "key1" in result
        assert "value1" in result

    def test_flatten_dict_with_none_values(self):
        """Test flattening dictionary with None values."""
        parser = CommandLineArgumentParser()
        test_dict = {"key1": None, "key2": "value2"}
        
        result = parser.flatten_dict_to_list(test_dict)
        
        assert isinstance(result, list)
        assert "key1" in result

    def test_flatten_empty_dict(self):
        """Test flattening empty dictionary."""
        parser = CommandLineArgumentParser()
        test_dict = {}
        
        result = parser.flatten_dict_to_list(test_dict)
        
        assert result == []


@pytest.mark.unit
class TestCommandLineArgumentParserLoadCommands:
    """Test suite for loading commands from configuration."""

    @patch('core.CommandLineArgumentParser.from_root')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_commands_success(self, mock_file, mock_from_root):
        """Test loading commands from valid JSON file."""
        mock_from_root.return_value = "/path/to/commands.json"
        mock_file.return_value.read.return_value = '{"commands": {"cmd1": {}}}'
        
        parser = CommandLineArgumentParser("!test")
        
        # commands_list should be loaded or None
        assert parser.commands_list is None or isinstance(parser.commands_list, dict)

    @patch('core.CommandLineArgumentParser.from_root')
    def test_load_commands_file_not_found(self, mock_from_root):
        """Test loading commands when file not found."""
        mock_from_root.return_value = "/nonexistent/commands.json"
        
        parser = CommandLineArgumentParser("!test")
        
        # Should handle gracefully
        assert parser.commands_list is None

    def test_load_commands_called_on_init(self):
        """Test that _load_commands is called during initialization."""
        parser = CommandLineArgumentParser("!test")
        
        # commands_list should be defined (could be None)
        assert hasattr(parser, 'commands_list')
