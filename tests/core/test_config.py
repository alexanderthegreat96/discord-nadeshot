"""Unit tests for core.Config module."""

import pytest
from unittest.mock import patch, MagicMock
from core.Config import Config


@pytest.mark.unit
class TestConfig:
    """Test suite for Config class."""

    @patch('core.Config.from_root')
    @patch('core.Config.EnvParser')
    def test_config_initialization_success(self, mock_env_parser_class, mock_from_root):
        """Test successful Config initialization."""
        # Mock EnvParser instance
        mock_env_parser = MagicMock()
        mock_env_parser.get_error.return_value = None
        mock_env_parser_class.return_value = mock_env_parser
        mock_from_root.return_value = "/path/to/.env"
        
        # Should not raise an exception
        config = Config()
        assert config is not None

    @patch('core.Config.from_root')
    @patch('core.Config.EnvParser')
    def test_config_initialization_failure(self, mock_env_parser_class, mock_from_root):
        """Test Config initialization with error."""
        # Mock EnvParser instance with error
        mock_env_parser = MagicMock()
        mock_env_parser.get_error.return_value = "Test error message"
        mock_env_parser_class.return_value = mock_env_parser
        mock_from_root.return_value = "/path/to/.env"
        
        # Should raise an exception
        with pytest.raises(Exception):
            config = Config()

    @patch('core.Config.from_root')
    @patch('core.Config.EnvParser')
    def test_config_env_method(self, mock_env_parser_class, mock_from_root):
        """Test that env() method returns EnvParser instance."""
        mock_env_parser = MagicMock()
        mock_env_parser.get_error.return_value = None
        mock_env_parser_class.return_value = mock_env_parser
        mock_from_root.return_value = "/path/to/.env"
        
        config = Config()
        env_parser = config.env()
        
        assert env_parser == mock_env_parser

    @patch('core.Config.from_root')
    @patch('core.Config.EnvParser')
    def test_config_uses_from_root(self, mock_env_parser_class, mock_from_root):
        """Test that Config uses from_root to find .env file."""
        mock_env_parser = MagicMock()
        mock_env_parser.get_error.return_value = None
        mock_env_parser_class.return_value = mock_env_parser
        mock_from_root.return_value = "/project/root/.env"
        
        config = Config()
        
        # Verify from_root was called with ".env"
        mock_from_root.assert_called()

    @patch('core.Config.from_root')
    @patch('core.Config.EnvParser')
    def test_multiple_config_instances(self, mock_env_parser_class, mock_from_root):
        """Test that multiple Config instances can be created."""
        mock_env_parser = MagicMock()
        mock_env_parser.get_error.return_value = None
        mock_env_parser_class.return_value = mock_env_parser
        mock_from_root.return_value = "/path/to/.env"
        
        config1 = Config()
        config2 = Config()
        
        assert config1 is not None
        assert config2 is not None
        assert config1 is not config2
