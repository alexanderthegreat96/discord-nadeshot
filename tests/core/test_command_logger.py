"""Unit tests for core.CommandLogger module."""

import pytest
from unittest.mock import MagicMock, patch
from core.CommandLogger import CommandLogger
from core.Logger import Logger


@pytest.mark.unit
class TestCommandLogger:
    """Test suite for CommandLogger class."""

    @patch("core.CommandLogger.Config")
    def test_command_logger_initialization(
        self, mock_config_class, mock_discord_context, mock_logger
    ):
        """Test CommandLogger initialization."""
        mock_config = MagicMock()
        mock_env = MagicMock()
        mock_env.get.return_value = "test-bot-v1"
        mock_config.env.return_value = mock_env
        mock_config_class.return_value = mock_config

        command_logger = CommandLogger(
            logger=mock_logger,
            context=mock_discord_context,
            command_data={"command": "test"},
        )

        assert command_logger.logger == mock_logger
        assert command_logger.command_data == {"command": "test"}

    @patch("core.CommandLogger.Config")
    def test_command_logger_without_command_data(
        self, mock_config_class, mock_discord_context, mock_logger
    ):
        """Test CommandLogger initialization without command_data."""
        mock_config = MagicMock()
        mock_env = MagicMock()
        mock_env.get.return_value = "test-bot-v1"
        mock_config.env.return_value = mock_env
        mock_config_class.return_value = mock_config

        command_logger = CommandLogger(logger=mock_logger, context=mock_discord_context)

        assert command_logger.command_data is None

    @patch("core.CommandLogger.Config")
    def test_command_logger_gets_bot_variant(
        self, mock_config_class, mock_discord_context, mock_logger
    ):
        """Test that CommandLogger retrieves bot variant from config."""
        mock_config = MagicMock()
        mock_env = MagicMock()
        mock_env.get.return_value = "custom-bot-variant"
        mock_config.env.return_value = mock_env
        mock_config_class.return_value = mock_config

        command_logger = CommandLogger(logger=mock_logger, context=mock_discord_context)

        assert command_logger.bot_variant == "custom-bot-variant"

    @patch("core.CommandLogger.Config")
    def test_command_logger_log_method(
        self, mock_config_class, mock_discord_context, mock_logger
    ):
        """Test that log method calls logger.info."""
        mock_config = MagicMock()
        mock_env = MagicMock()
        mock_env.get.return_value = "test-bot-v1"
        mock_config.env.return_value = mock_env
        mock_config_class.return_value = mock_config

        command_logger = CommandLogger(
            logger=mock_logger,
            context=mock_discord_context,
            command_data={"action": "test_action"},
        )

        command_logger.log()

        # Verify logger.info was called
        mock_logger.info.assert_called_once()

    @patch("core.CommandLogger.Config")
    def test_command_logger_creates_message_wrapper(
        self, mock_config_class, mock_discord_context, mock_logger
    ):
        """Test that CommandLogger creates MessageWrapper."""
        mock_config = MagicMock()
        mock_env = MagicMock()
        mock_env.get.return_value = "test-bot-v1"
        mock_config.env.return_value = mock_env
        mock_config_class.return_value = mock_config

        command_logger = CommandLogger(logger=mock_logger, context=mock_discord_context)

        assert command_logger.message_wrapper is not None
