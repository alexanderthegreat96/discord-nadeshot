"""Unit tests for services.DiscordApi module."""

import pytest
from unittest.mock import MagicMock, patch
from services.DiscordApi import DiscordApi


@pytest.mark.unit
class TestDiscordApiInitialization:
    """Test suite for DiscordApi initialization."""

    @patch('services.DiscordApi.EnvParser')
    @patch('services.DiscordApi.from_root')
    @patch('services.DiscordApi.Logger')
    def test_discord_api_initialization(self, mock_logger_class, mock_from_root, mock_env_parser_class):
        """Test DiscordApi initialization."""
        mock_env = MagicMock()
        mock_env.get.return_value = "test_token_123"
        mock_env_parser_class.return_value = mock_env
        mock_from_root.return_value = "/path/.env"
        mock_logger = MagicMock()
        mock_logger_class.return_value.get_logger.return_value = mock_logger
        
        api = DiscordApi()
        
        assert api.bot_token == "test_token_123"
        assert api.api_base_url == "https://discord.com/api/v10"

    @patch('services.DiscordApi.EnvParser')
    @patch('services.DiscordApi.from_root')
    @patch('services.DiscordApi.Logger')
    def test_discord_api_has_logger(self, mock_logger_class, mock_from_root, mock_env_parser_class):
        """Test that DiscordApi has logger configured."""
        mock_env = MagicMock()
        mock_env.get.return_value = "test_token"
        mock_env_parser_class.return_value = mock_env
        mock_from_root.return_value = "/path/.env"
        mock_logger = MagicMock()
        mock_logger_class.return_value.get_logger.return_value = mock_logger
        
        api = DiscordApi()
        
        assert api.logger is not None


@pytest.mark.unit
class TestDiscordApiConstants:
    """Test suite for DiscordApi constants."""

    def test_discord_api_epoch_constant(self):
        """Test Discord epoch constant is correct."""
        assert DiscordApi.DISCORD_EPOCH == 1420070400000

    def test_discord_api_max_retries_constant(self):
        """Test max retries constant."""
        assert DiscordApi.MAX_RETRIES == 5

    def test_discord_api_retry_delay_constant(self):
        """Test retry delay constant."""
        assert DiscordApi.RETRY_DELAY == 2

    def test_discord_api_has_retry_request_decorator(self):
        """Test that DiscordApi has retry_request decorator."""
        assert hasattr(DiscordApi, 'retry_request')


@pytest.mark.unit
class TestDiscordApiMethods:
    """Test suite for DiscordApi methods."""

    @patch('services.DiscordApi.EnvParser')
    @patch('services.DiscordApi.from_root')
    @patch('services.DiscordApi.Logger')
    def test_discord_api_attributes(self, mock_logger_class, mock_from_root, mock_env_parser_class):
        """Test DiscordApi has expected attributes."""
        mock_env = MagicMock()
        mock_env.get.return_value = "test_token"
        mock_env_parser_class.return_value = mock_env
        mock_from_root.return_value = "/path/.env"
        mock_logger = MagicMock()
        mock_logger_class.return_value.get_logger.return_value = mock_logger
        
        api = DiscordApi()
        
        assert hasattr(api, 'api_base_url')
        assert hasattr(api, 'bot_token')
        assert hasattr(api, 'logger')
