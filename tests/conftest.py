"""Pytest configuration and shared fixtures for test suite."""

import os
import sys
import pytest
from unittest.mock import Mock, MagicMock
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def mock_env_file(tmp_path):
    """Create a temporary .env file for testing."""
    env_file = tmp_path / ".env"
    env_content = """
BOT_TOKEN=test_token_12345
BOT_PREFIX=!
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASS=test_password
REDIS_GLOBAL_CACHE_KEY=test-bot
BOT_VARIANT=test-v1
"""
    env_file.write_text(env_content.strip())
    return str(env_file)


@pytest.fixture
def mock_config_file(tmp_path):
    """Create a temporary config.json file for testing."""
    config_file = tmp_path / "config.json"
    config_content = """{
    "bot_name": "Test Bot",
    "version": "2.0.0",
    "debug": true
}"""
    config_file.write_text(config_content)
    return config_file


@pytest.fixture
def mock_logger():
    """Create a mock logger for testing."""
    logger = MagicMock()
    logger.debug = MagicMock()
    logger.info = MagicMock()
    logger.warning = MagicMock()
    logger.error = MagicMock()
    logger.success = MagicMock()
    return logger


@pytest.fixture
def mock_discord_message():
    """Create a mock Discord message."""
    message = MagicMock()
    message.content = "!test command"
    message.author = MagicMock()
    message.author.id = 123456789
    message.author.name = "TestUser"
    message.guild = MagicMock()
    message.guild.id = 987654321
    message.guild.name = "TestGuild"
    message.channel = MagicMock()
    message.channel.id = 555555555
    return message


@pytest.fixture
def mock_discord_context(mock_discord_message):
    """Create a mock Discord context."""
    ctx = MagicMock()
    ctx.message = mock_discord_message
    ctx.author = mock_discord_message.author
    ctx.guild = mock_discord_message.guild
    ctx.channel = mock_discord_message.channel
    ctx.send = MagicMock()
    ctx.reply = MagicMock()
    return ctx


@pytest.fixture
def mock_redis():
    """Create a mock Redis client."""
    redis_mock = MagicMock()
    redis_mock.set = MagicMock(return_value=True)
    redis_mock.get = MagicMock(return_value=b"test_value")
    redis_mock.delete = MagicMock(return_value=True)
    redis_mock.exists = MagicMock(return_value=True)
    redis_mock.lpush = MagicMock(return_value=1)
    redis_mock.rpop = MagicMock(return_value=b"item")
    return redis_mock
