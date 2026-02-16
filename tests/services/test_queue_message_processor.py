"""Unit tests for services.QueueMessageProcessor module."""

import pytest
from unittest.mock import MagicMock, patch
from services.QueueMessageProcessor import QueueMessageProcessor


@pytest.mark.unit
class TestQueueMessageProcessorInitialization:
    """Test suite for QueueMessageProcessor initialization."""

    def test_queue_message_processor_initialization(self, mock_logger):
        """Test QueueMessageProcessor initialization."""
        processor = QueueMessageProcessor(mock_logger)

        assert processor.logger == mock_logger
        assert processor.cache is not None
        assert processor.config is not None

    def test_queue_message_processor_has_cache(self, mock_logger):
        """Test that QueueMessageProcessor has cache instance."""
        processor = QueueMessageProcessor(mock_logger)

        assert hasattr(processor, "cache")

    def test_queue_message_processor_has_config(self, mock_logger):
        """Test that QueueMessageProcessor has config instance."""
        processor = QueueMessageProcessor(mock_logger)

        assert hasattr(processor, "config")

    def test_queue_message_processor_has_logger(self, mock_logger):
        """Test that QueueMessageProcessor stores logger."""
        processor = QueueMessageProcessor(mock_logger)

        assert processor.logger == mock_logger


@pytest.mark.unit
class TestQueueMessageProcessorPrivateMethods:
    """Test suite for QueueMessageProcessor private methods."""

    @patch("services.QueueMessageProcessor.Cache")
    @patch("services.QueueMessageProcessor.Config")
    def test_queue_message_processor_get_queue_name_missing_raises_error(
        self, mock_config_class, mock_cache_class, mock_logger
    ):
        """Test that __get_queue_name raises ValueError when queue name not found."""
        mock_cache = MagicMock()
        mock_cache_class.return_value = mock_cache

        mock_config = MagicMock()
        mock_env = MagicMock()
        mock_env.get.return_value = None
        mock_config.env.return_value = mock_env
        mock_config_class.return_value = mock_config

        processor = QueueMessageProcessor(mock_logger)

        # Access private method for testing
        with pytest.raises(ValueError):
            processor._QueueMessageProcessor__get_queue_name("NONEXISTENT_QUEUE")

    @patch("services.QueueMessageProcessor.Cache")
    @patch("services.QueueMessageProcessor.Config")
    def test_queue_message_processor_get_queue_name_success(
        self, mock_config_class, mock_cache_class, mock_logger
    ):
        """Test __get_queue_name returns queue name successfully."""
        mock_cache = MagicMock()
        mock_cache_class.return_value = mock_cache

        mock_config = MagicMock()
        mock_env = MagicMock()
        mock_env.get.return_value = "test_queue_name"
        mock_config.env.return_value = mock_env
        mock_config_class.return_value = mock_config

        processor = QueueMessageProcessor(mock_logger)

        # Access private method for testing
        queue_name = processor._QueueMessageProcessor__get_queue_name("TEST_QUEUE_VAR")
        assert queue_name == "test_queue_name"


@pytest.mark.unit
class TestQueueMessageProcessorMethods:
    """Test suite for QueueMessageProcessor public methods."""

    def test_queue_message_processor_has_send_to_queue_method(self, mock_logger):
        """Test that QueueMessageProcessor has send_to_queue method."""
        processor = QueueMessageProcessor(mock_logger)

        assert hasattr(processor, "send_to_queue")
        assert callable(processor.send_to_queue)

    def test_queue_message_processor_has_process_queue_method(self, mock_logger):
        """Test that QueueMessageProcessor has process_queue method."""
        processor = QueueMessageProcessor(mock_logger)

        assert hasattr(processor, "process_queue")
        assert callable(processor.process_queue)

    def test_queue_message_processor_logger_is_accessible(self, mock_logger):
        """Test that logger is accessible after initialization."""
        processor = QueueMessageProcessor(mock_logger)

        assert processor.logger is mock_logger
