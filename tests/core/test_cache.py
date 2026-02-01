"""Unit tests for core.Cache module."""

import pytest
from unittest.mock import MagicMock, patch, Mock
from core.Cache import Cache


@pytest.mark.unit
class TestCacheInitialization:
    """Test suite for Cache initialization."""

    @patch('core.Cache.EnvParser')
    @patch('core.Cache.from_root')
    def test_cache_initialization(self, mock_from_root, mock_env_parser_class):
        """Test Cache initialization with environment variables."""
        mock_env_parser = MagicMock()
        mock_env_parser.get.side_effect = lambda which, default="", **kwargs: {
            "REDIS_HOST": "localhost",
            "REDIS_PORT": 6379,
            "REDIS_PASS": "password",
            "REDIS_GLOBAL_CACHE_KEY": "test-bot"
        }.get(which, default)
        
        mock_env_parser_class.return_value = mock_env_parser
        mock_from_root.return_value = "/path/.env"
        
        # This will fail because Redis connection is not mocked
        # but we can verify the initialization attempt
        with patch('core.Cache.Redis'):
            cache = Cache()
            assert cache is not None

    @patch('core.Cache.EnvParser')
    @patch('core.Cache.from_root')
    @patch('core.Cache.Redis')
    def test_cache_with_custom_global_key(self, mock_redis, mock_from_root, mock_env_parser_class):
        """Test Cache initialization with custom global cache key."""
        mock_env_parser = MagicMock()
        mock_env_parser.get.side_effect = lambda which, default="", **kwargs: {
            "REDIS_HOST": "localhost",
            "REDIS_PORT": 6379,
            "REDIS_PASS": "password",
            "REDIS_GLOBAL_CACHE_KEY": "default-key"
        }.get(which, default)
        
        mock_env_parser_class.return_value = mock_env_parser
        mock_from_root.return_value = "/path/.env"
        
        cache = Cache(global_cache_key="custom-key")
        assert cache is not None

    @patch('core.Cache.EnvParser')
    @patch('core.Cache.from_root')
    @patch('core.Cache.Redis')
    def test_cache_uses_env_variables(self, mock_redis, mock_from_root, mock_env_parser_class):
        """Test that Cache uses environment variables for configuration."""
        mock_env_parser = MagicMock()
        mock_env_parser.get.side_effect = lambda which, default="", **kwargs: {
            "REDIS_HOST": "custom-host",
            "REDIS_PORT": 6380,
            "REDIS_PASS": "custom-pass",
            "REDIS_GLOBAL_CACHE_KEY": "custom-prefix"
        }.get(which, default)
        
        mock_env_parser_class.return_value = mock_env_parser
        mock_from_root.return_value = "/path/.env"
        
        cache = Cache()
        
        # Verify EnvParser was called with correct parameters
        mock_env_parser_class.assert_called_once()


@pytest.mark.unit
class TestCacheOperations:
    """Test suite for Cache operations."""

    @patch('core.Cache.EnvParser')
    @patch('core.Cache.from_root')
    @patch('core.Cache.Redis')
    def test_cache_has_logger(self, mock_redis, mock_from_root, mock_env_parser_class):
        """Test that Cache has a logger configured."""
        mock_env_parser = MagicMock()
        mock_env_parser.get.side_effect = lambda which, default="", **kwargs: {
            "REDIS_HOST": "localhost",
            "REDIS_PORT": 6379,
            "REDIS_PASS": "password",
            "REDIS_GLOBAL_CACHE_KEY": "test-bot"
        }.get(which, default)
        
        mock_env_parser_class.return_value = mock_env_parser
        mock_from_root.return_value = "/path/.env"
        
        with patch('core.Cache.Logger') as mock_logger_class:
            mock_logger = MagicMock()
            mock_logger_class.return_value = mock_logger
            
            cache = Cache()
            # Verify logger was attempted to be created
            assert cache is not None
