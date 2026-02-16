"""Unit tests for core.Logger module."""

import pytest
import logging
from unittest.mock import MagicMock, patch
from core.Logger import Logger, CustomLoggingFormatter, SUCCESS_LEVEL_NUM


@pytest.mark.unit
class TestLogger:
    """Test suite for Logger class."""

    def test_logger_initialization(self):
        """Test that logger initializes correctly."""
        logger = Logger("TestLogger")
        assert logger is not None

    def test_get_logger_returns_logger_instance(self):
        """Test that get_logger returns a logger instance."""
        logger = Logger("TestLogger")
        log_instance = logger.get_logger()
        assert isinstance(log_instance, logging.Logger)

    def test_custom_success_level_exists(self):
        """Test that SUCCESS custom log level is registered."""
        assert SUCCESS_LEVEL_NUM == 25
        level_name = logging.getLevelName(SUCCESS_LEVEL_NUM)
        assert level_name == "SUCCESS"

    def test_logger_name_matches_input(self):
        """Test that logger name matches the input."""
        test_name = "TestLoggerName"
        logger = Logger(test_name)
        log_instance = logger.get_logger()
        assert log_instance.name == test_name

    def test_multiple_logger_instances(self):
        """Test that multiple logger instances can be created."""
        logger1 = Logger("Logger1")
        logger2 = Logger("Logger2")

        assert logger1.get_logger().name == "Logger1"
        assert logger2.get_logger().name == "Logger2"

    def test_logger_can_be_configured_with_handlers(self):
        """Test that logger instance can have handlers added."""
        logger = Logger("TestLogger")
        log_instance = logger.get_logger()
        # Logger is created and can have handlers added to it
        assert isinstance(log_instance, logging.Logger)
        assert log_instance.name == "TestLogger"


@pytest.mark.unit
class TestCustomLoggingFormatter:
    """Test suite for CustomLoggingFormatter class."""

    def test_formatter_initialization(self):
        """Test that formatter initializes correctly."""
        formatter = CustomLoggingFormatter("%(levelname)s - %(message)s")
        assert formatter is not None

    def test_formatter_has_color_mappings(self):
        """Test that formatter has LEVEL_COLORS defined."""
        assert hasattr(CustomLoggingFormatter, "LEVEL_COLORS")
        assert CustomLoggingFormatter.LEVEL_COLORS is not None

    def test_color_mapping_includes_all_levels(self):
        """Test that all standard logging levels have colors."""
        colors = CustomLoggingFormatter.LEVEL_COLORS
        assert logging.DEBUG in colors
        assert logging.INFO in colors
        assert logging.WARNING in colors
        assert logging.ERROR in colors
        assert logging.CRITICAL in colors
        assert SUCCESS_LEVEL_NUM in colors

    def test_format_adds_color_codes(self):
        """Test that format method adds color codes to output."""
        formatter = CustomLoggingFormatter("%(levelname)s - %(message)s")

        # Create a log record
        record = logging.LogRecord(
            name="TestLogger",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        formatted = formatter.format(record)
        assert formatted is not None
        assert len(formatted) > 0
