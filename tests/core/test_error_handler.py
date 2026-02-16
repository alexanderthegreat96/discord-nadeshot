"""Unit tests for core.ErrorHandler module."""

import pytest
from unittest.mock import MagicMock
from core.ErrorHandler import ErrorHandler
from core.Logger import Logger


@pytest.mark.unit
class TestErrorHandler:
    """Test suite for ErrorHandler class."""

    def test_error_handler_initialization_with_context(
        self, mock_discord_context, mock_logger
    ):
        """Test ErrorHandler initialization with context."""
        error_message = "Test error"
        traceback_str = "Traceback: test"

        handler = ErrorHandler(
            ctx=mock_discord_context,
            error=error_message,
            traceback=traceback_str,
            logger=mock_logger,
        )

        assert handler.context == mock_discord_context
        assert handler.error == error_message
        assert handler.traceback == traceback_str
        assert handler.logger == mock_logger

    def test_error_handler_initialization_without_context(self, mock_logger):
        """Test ErrorHandler initialization without context."""
        error_message = "Test error"
        traceback_str = "Traceback: test"

        handler = ErrorHandler(
            ctx=None, error=error_message, traceback=traceback_str, logger=mock_logger
        )

        assert handler.context is None
        assert handler.error == error_message

    def test_error_handler_extracts_message_content(
        self, mock_discord_context, mock_logger
    ):
        """Test that ErrorHandler extracts message content from context."""
        handler = ErrorHandler(
            ctx=mock_discord_context,
            error="Test error",
            traceback="Traceback",
            logger=mock_logger,
        )

        assert handler.message == mock_discord_context.message
        assert handler.message_content == "!test command"

    def test_error_handler_message_wrapper_creation(
        self, mock_discord_context, mock_logger
    ):
        """Test that MessageWrapper is created when message exists."""
        handler = ErrorHandler(
            ctx=mock_discord_context,
            error="Test error",
            traceback="Traceback",
            logger=mock_logger,
        )

        assert handler.message_wrapper is not None

    def test_error_handler_message_wrapper_none_when_no_message(self, mock_logger):
        """Test that MessageWrapper is None when no message in context."""
        ctx = MagicMock()
        ctx.message = None

        handler = ErrorHandler(
            ctx=ctx, error="Test error", traceback="Traceback", logger=mock_logger
        )

        assert handler.message_wrapper is None

    def test_error_handler_stores_all_parameters(
        self, mock_discord_context, mock_logger
    ):
        """Test that ErrorHandler stores all parameters correctly."""
        error = "Critical error"
        traceback = "Full traceback here"

        handler = ErrorHandler(
            ctx=mock_discord_context,
            error=error,
            traceback=traceback,
            logger=mock_logger,
        )

        assert handler.error == error
        assert handler.traceback == traceback
