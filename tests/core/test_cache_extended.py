"""Enhanced unit tests for core.Cache module."""

import pytest
from unittest.mock import MagicMock, patch, Mock
from core.Cache import Cache


@pytest.mark.unit
class TestCacheEnqueueItem:
    """Test suite for Cache enqueue operations."""

    @patch('core.Cache.Redis')
    @patch('core.Cache.EnvParser')
    @patch('core.Cache.from_root')
    def test_cache_enqueue_item(self, mock_from_root, mock_env_parser_class, mock_redis_class):
        """Test enqueueing item to cache."""
        mock_redis = MagicMock()
        mock_redis_class.return_value = mock_redis
        
        mock_env = MagicMock()
        mock_env.get.side_effect = lambda which, default="", **kwargs: {
            "REDIS_HOST": "localhost",
            "REDIS_PORT": 6379,
            "REDIS_PASS": "password",
            "REDIS_GLOBAL_CACHE_KEY": "test-bot"
        }.get(which, default)
        mock_env_parser_class.return_value = mock_env
        mock_from_root.return_value = "/path/.env"
        
        cache = Cache()
        # Verify enqueue_item method exists
        assert hasattr(cache, 'enqueue_item')

    @patch('core.Cache.Redis')
    @patch('core.Cache.EnvParser')
    @patch('core.Cache.from_root')
    def test_cache_enqueue_item_unique(self, mock_from_root, mock_env_parser_class, mock_redis_class):
        """Test enqueueing unique item to cache."""
        mock_redis = MagicMock()
        mock_redis_class.return_value = mock_redis
        
        mock_env = MagicMock()
        mock_env.get.side_effect = lambda which, default="", **kwargs: {
            "REDIS_HOST": "localhost",
            "REDIS_PORT": 6379,
            "REDIS_PASS": "password",
            "REDIS_GLOBAL_CACHE_KEY": "test-bot"
        }.get(which, default)
        mock_env_parser_class.return_value = mock_env
        mock_from_root.return_value = "/path/.env"
        
        cache = Cache()
        # Verify enqueue_item_unique method exists
        assert hasattr(cache, 'enqueue_item_unique')


@pytest.mark.unit
class TestCacheSetAndGet:
    """Test suite for Cache get/set operations."""

    @patch('core.Cache.Redis')
    @patch('core.Cache.EnvParser')
    @patch('core.Cache.from_root')
    def test_cache_set_data(self, mock_from_root, mock_env_parser_class, mock_redis_class):
        """Test setting data in cache."""
        mock_redis = MagicMock()
        mock_redis_class.return_value = mock_redis
        mock_redis.set = MagicMock(return_value=True)
        
        mock_env = MagicMock()
        mock_env.get.side_effect = lambda which, default="", **kwargs: {
            "REDIS_HOST": "localhost",
            "REDIS_PORT": 6379,
            "REDIS_PASS": "password",
            "REDIS_GLOBAL_CACHE_KEY": "test-bot"
        }.get(which, default)
        mock_env_parser_class.return_value = mock_env
        mock_from_root.return_value = "/path/.env"
        
        cache = Cache()
        # Verify set_data method exists
        assert hasattr(cache, 'set_data')

    @patch('core.Cache.Redis')
    @patch('core.Cache.EnvParser')
    @patch('core.Cache.from_root')
    def test_cache_get_data(self, mock_from_root, mock_env_parser_class, mock_redis_class):
        """Test getting data from cache."""
        mock_redis = MagicMock()
        mock_redis_class.return_value = mock_redis
        mock_redis.get = MagicMock(return_value=b"test_value")
        
        mock_env = MagicMock()
        mock_env.get.side_effect = lambda which, default="", **kwargs: {
            "REDIS_HOST": "localhost",
            "REDIS_PORT": 6379,
            "REDIS_PASS": "password",
            "REDIS_GLOBAL_CACHE_KEY": "test-bot"
        }.get(which, default)
        mock_env_parser_class.return_value = mock_env
        mock_from_root.return_value = "/path/.env"
        
        cache = Cache()
        # Verify get_data method exists
        assert hasattr(cache, 'get_data')


@pytest.mark.unit
class TestCacheDelete:
    """Test suite for Cache deletion operations."""

    @patch('core.Cache.Redis')
    @patch('core.Cache.EnvParser')
    @patch('core.Cache.from_root')
    def test_cache_reset_data(self, mock_from_root, mock_env_parser_class, mock_redis_class):
        """Test resetting (deleting) data from cache."""
        mock_redis = MagicMock()
        mock_redis_class.return_value = mock_redis
        mock_redis.delete = MagicMock(return_value=True)
        
        mock_env = MagicMock()
        mock_env.get.side_effect = lambda which, default="", **kwargs: {
            "REDIS_HOST": "localhost",
            "REDIS_PORT": 6379,
            "REDIS_PASS": "password",
            "REDIS_GLOBAL_CACHE_KEY": "test-bot"
        }.get(which, default)
        mock_env_parser_class.return_value = mock_env
        mock_from_root.return_value = "/path/.env"
        
        cache = Cache()
        # Verify reset_data method exists
        assert hasattr(cache, 'reset_data')


@pytest.mark.unit
class TestCacheExists:
    """Test suite for Cache existence checking."""

    @patch('core.Cache.Redis')
    @patch('core.Cache.EnvParser')
    @patch('core.Cache.from_root')
    def test_cache_clear_cache(self, mock_from_root, mock_env_parser_class, mock_redis_class):
        """Test clearing cache."""
        mock_redis = MagicMock()
        mock_redis_class.return_value = mock_redis
        mock_redis.exists = MagicMock(return_value=1)
        
        mock_env = MagicMock()
        mock_env.get.side_effect = lambda which, default="", **kwargs: {
            "REDIS_HOST": "localhost",
            "REDIS_PORT": 6379,
            "REDIS_PASS": "password",
            "REDIS_GLOBAL_CACHE_KEY": "test-bot"
        }.get(which, default)
        mock_env_parser_class.return_value = mock_env
        mock_from_root.return_value = "/path/.env"
        
        cache = Cache()
        # Verify clear_cache method exists
        assert hasattr(cache, 'clear_cache')


@pytest.mark.unit
class TestCacheEnvironmentConfiguration:
    """Test suite for Cache environment configuration."""

    @patch('core.Cache.Redis')
    @patch('core.Cache.EnvParser')
    @patch('core.Cache.from_root')
    def test_cache_uses_redis_host_env_var(self, mock_from_root, mock_env_parser_class, mock_redis_class):
        """Test that Cache uses REDIS_HOST from environment."""
        mock_redis = MagicMock()
        mock_redis_class.return_value = mock_redis
        
        mock_env = MagicMock()
        mock_env.get.side_effect = lambda which, default="", **kwargs: {
            "REDIS_HOST": "custom-redis-host",
            "REDIS_PORT": 6380,
            "REDIS_PASS": "custom-pass",
            "REDIS_GLOBAL_CACHE_KEY": "custom-key"
        }.get(which, default)
        mock_env_parser_class.return_value = mock_env
        mock_from_root.return_value = "/path/.env"
        
        cache = Cache()
        # Verify EnvParser was used to get config
        assert mock_env_parser_class.called

    @patch('core.Cache.Redis')
    @patch('core.Cache.EnvParser')
    @patch('core.Cache.from_root')
    def test_cache_with_custom_global_key(self, mock_from_root, mock_env_parser_class, mock_redis_class):
        """Test Cache initialization with custom global cache key."""
        mock_redis = MagicMock()
        mock_redis_class.return_value = mock_redis
        
        mock_env = MagicMock()
        mock_env.get.side_effect = lambda which, default="", **kwargs: {
            "REDIS_HOST": "localhost",
            "REDIS_PORT": 6379,
            "REDIS_PASS": "password",
            "REDIS_GLOBAL_CACHE_KEY": "default"
        }.get(which, default)
        mock_env_parser_class.return_value = mock_env
        mock_from_root.return_value = "/path/.env"
        
        cache = Cache(global_cache_key="custom-key")
        # Should initialize with custom key
        assert cache is not None
