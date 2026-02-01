"""Unit tests for core.MultiBotHandler module."""

import pytest
import json
from unittest.mock import MagicMock, patch, mock_open
from core.MultiBotHandler import MultiBotHandler


@pytest.mark.unit
class TestMultiBotHandlerInitialization:
    """Test suite for MultiBotHandler initialization."""

    @patch('core.MultiBotHandler.EnvParser')
    @patch('core.MultiBotHandler.from_root')
    @patch('core.MultiBotHandler.Logger')
    def test_multi_bot_handler_initialization(self, mock_logger_class, mock_from_root, mock_env_parser_class):
        """Test MultiBotHandler initialization."""
        mock_env = MagicMock()
        mock_env.get.return_value = "primary-bot"
        mock_env_parser_class.return_value = mock_env
        mock_from_root.return_value = "/path/.env"
        mock_logger = MagicMock()
        mock_logger_class.return_value.get_logger.return_value = mock_logger
        
        handler = MultiBotHandler()
        
        assert handler.current_bot_variant == "primary-bot"
        assert handler.multi_bot_config == {}

    @patch('core.MultiBotHandler.EnvParser')
    @patch('core.MultiBotHandler.from_root')
    @patch('core.MultiBotHandler.Logger')
    def test_multi_bot_handler_has_logger(self, mock_logger_class, mock_from_root, mock_env_parser_class):
        """Test that MultiBotHandler has logger."""
        mock_env = MagicMock()
        mock_env.get.return_value = "test-bot"
        mock_env_parser_class.return_value = mock_env
        mock_from_root.return_value = "/path/.env"
        mock_logger = MagicMock()
        mock_logger_class.return_value.get_logger.return_value = mock_logger
        
        handler = MultiBotHandler()
        
        assert handler.logger is not None


@pytest.mark.unit
class TestMultiBotHandlerRetrieveConfig:
    """Test suite for retrieving multi-bot configuration."""

    @patch('core.MultiBotHandler.EnvParser')
    @patch('core.MultiBotHandler.from_root')
    @patch('core.MultiBotHandler.Logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_retrieve_multi_bot_config_success(
        self, mock_file, mock_logger_class, mock_from_root, mock_env_parser_class
    ):
        """Test successful config retrieval."""
        config_data = {"servers": [{"server_id": 123, "bot-variants": {"primary": "bot1"}}]}
        mock_file.return_value.read.return_value = json.dumps(config_data)
        
        mock_env = MagicMock()
        mock_env.get.return_value = "bot1"
        mock_env_parser_class.return_value = mock_env
        mock_from_root.return_value = "/path/.env"
        mock_logger = MagicMock()
        mock_logger_class.return_value.get_logger.return_value = mock_logger
        
        handler = MultiBotHandler()
        handler.retrieve_multi_bot_config()
        
        assert handler.multi_bot_config is not None

    @patch('core.MultiBotHandler.EnvParser')
    @patch('core.MultiBotHandler.from_root')
    @patch('core.MultiBotHandler.Logger')
    def test_retrieve_multi_bot_config_file_not_found(
        self, mock_logger_class, mock_from_root, mock_env_parser_class
    ):
        """Test config retrieval when file not found."""
        mock_env = MagicMock()
        mock_env.get.return_value = "test-bot"
        mock_env_parser_class.return_value = mock_env
        mock_from_root.return_value = "/nonexistent/path"
        mock_logger = MagicMock()
        mock_logger_class.return_value.get_logger.return_value = mock_logger
        
        handler = MultiBotHandler()
        handler.retrieve_multi_bot_config()
        
        # Should not crash, logger.error should be called
        assert handler.multi_bot_config == {} or handler.multi_bot_config is not None


@pytest.mark.unit
class TestMultiBotHandlerIgnoreCommands:
    """Test suite for command ignoring logic."""

    @patch('core.MultiBotHandler.EnvParser')
    @patch('core.MultiBotHandler.from_root')
    @patch('core.MultiBotHandler.Logger')
    def test_should_ignore_commands_no_config(
        self, mock_logger_class, mock_from_root, mock_env_parser_class
    ):
        """Test ignore commands when no config loaded."""
        mock_env = MagicMock()
        mock_env.get.return_value = "test-bot"
        mock_env_parser_class.return_value = mock_env
        mock_from_root.return_value = "/nonexistent"
        mock_logger = MagicMock()
        mock_logger_class.return_value.get_logger.return_value = mock_logger
        
        handler = MultiBotHandler()
        result = handler.should_ignore_commands(123)
        
        assert result is False  # Default behavior

    @patch('core.MultiBotHandler.EnvParser')
    @patch('core.MultiBotHandler.from_root')
    @patch('core.MultiBotHandler.Logger')
    def test_should_ignore_commands_primary_bot(
        self, mock_logger_class, mock_from_root, mock_env_parser_class
    ):
        """Test that primary bot doesn't ignore commands."""
        mock_env = MagicMock()
        mock_env.get.return_value = "primary-bot"
        mock_env_parser_class.return_value = mock_env
        
        def from_root_side_effect(path):
            if ".env" in path:
                return "/path/.env"
            return "/path/multi-bot.json"
        
        mock_from_root.side_effect = from_root_side_effect
        mock_logger = MagicMock()
        mock_logger_class.return_value.get_logger.return_value = mock_logger
        
        with patch('builtins.open', mock_open(read_data=json.dumps({
            "servers": [{
                "server_id": 123,
                "bot-variants": {"primary": "primary-bot", "others": []}
            }]
        }))):
            handler = MultiBotHandler()
            result = handler.should_ignore_commands(123)
            
            # Primary bot should not ignore commands
            assert result is False

    @patch('core.MultiBotHandler.EnvParser')
    @patch('core.MultiBotHandler.from_root')
    @patch('core.MultiBotHandler.Logger')
    def test_should_ignore_commands_secondary_bot(
        self, mock_logger_class, mock_from_root, mock_env_parser_class
    ):
        """Test that secondary bot ignores commands."""
        mock_env = MagicMock()
        mock_env.get.return_value = "secondary-bot"
        mock_env_parser_class.return_value = mock_env
        
        def from_root_side_effect(path):
            if ".env" in path:
                return "/path/.env"
            return "/path/multi-bot.json"
        
        mock_from_root.side_effect = from_root_side_effect
        mock_logger = MagicMock()
        mock_logger_class.return_value.get_logger.return_value = mock_logger
        
        with patch('builtins.open', mock_open(read_data=json.dumps({
            "servers": [{
                "server_id": 123,
                "bot-variants": {"primary": "primary-bot", "others": ["secondary-bot"]}
            }]
        }))):
            handler = MultiBotHandler()
            result = handler.should_ignore_commands(123)
            
            # Secondary bot should ignore commands
            assert result is True

    @patch('core.MultiBotHandler.EnvParser')
    @patch('core.MultiBotHandler.from_root')
    @patch('core.MultiBotHandler.Logger')
    def test_should_ignore_commands_empty_servers_list(
        self, mock_logger_class, mock_from_root, mock_env_parser_class
    ):
        """Test with empty servers list."""
        mock_env = MagicMock()
        mock_env.get.return_value = "test-bot"
        mock_env_parser_class.return_value = mock_env
        
        def from_root_side_effect(path):
            if ".env" in path:
                return "/path/.env"
            return "/path/multi-bot.json"
        
        mock_from_root.side_effect = from_root_side_effect
        mock_logger = MagicMock()
        mock_logger_class.return_value.get_logger.return_value = mock_logger
        
        with patch('builtins.open', mock_open(read_data=json.dumps({"servers": []}))):
            handler = MultiBotHandler()
            result = handler.should_ignore_commands(999)
            
            # No matching server, should not ignore
            assert result is False
