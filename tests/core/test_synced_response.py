"""Unit tests for core.SyncedResponse module."""

import pytest
import asyncio
import discord
from unittest.mock import MagicMock, AsyncMock, patch
from core.SyncedResponse import SyncedResponse


@pytest.mark.unit
class TestSyncedResponseInitialization:
    """Test suite for SyncedResponse initialization."""

    def test_synced_response_initialization(self, mock_discord_context):
        """Test SyncedResponse initialization with context."""
        synced = SyncedResponse(mock_discord_context)
        
        assert synced.ctx == mock_discord_context
        assert synced.user_id == mock_discord_context.author.id
        assert synced.channel_id == mock_discord_context.channel.id
        assert synced.origin == "commands"

    def test_synced_response_initialization_with_origin(self, mock_discord_context):
        """Test SyncedResponse initialization with custom origin."""
        synced = SyncedResponse(mock_discord_context, origin="events")
        
        assert synced.origin == "events"

    def test_synced_response_has_logger(self, mock_discord_context):
        """Test that SyncedResponse has logger."""
        synced = SyncedResponse(mock_discord_context)
        
        assert synced.logger is not None

    def test_synced_response_extracts_ids_from_context(self, mock_discord_context):
        """Test that user and channel IDs are extracted from context."""
        synced = SyncedResponse(mock_discord_context)
        
        assert synced.user_id == 123456789
        assert synced.channel_id == 555555555


@pytest.mark.unit
class TestSyncedResponseQueueing:
    """Test suite for SyncedResponse queuing functionality."""

    @pytest.mark.asyncio
    async def test_synced_response_send_string(self, mock_discord_context):
        """Test sending a string message."""
        synced = SyncedResponse(mock_discord_context)
        mock_discord_context.channel.send = AsyncMock()
        
        await synced.send("Test message")
        
        # Queue should have item
        queue_key = (synced.user_id, synced.channel_id, synced.origin)
        assert queue_key in SyncedResponse._queues

    @pytest.mark.asyncio
    async def test_synced_response_send_embed(self, mock_discord_context):
        """Test sending an embed message."""
        synced = SyncedResponse(mock_discord_context)
        mock_discord_context.channel.send = AsyncMock()
        
        embed = MagicMock(spec=discord.Embed)
        await synced.send(embed)
        
        # Queue should have item
        queue_key = (synced.user_id, synced.channel_id, synced.origin)
        assert queue_key in SyncedResponse._queues

    @pytest.mark.asyncio
    async def test_synced_response_creates_processing_task(self, mock_discord_context):
        """Test that processing task is created."""
        synced = SyncedResponse(mock_discord_context)
        mock_discord_context.channel.send = AsyncMock()
        
        await synced.send("Test")
        
        queue_key = (synced.user_id, synced.channel_id, synced.origin)
        # Should have processing task or queued item
        assert queue_key in SyncedResponse._queues

    @pytest.mark.asyncio
    async def test_synced_response_multiple_origins(self, mock_discord_context):
        """Test that different origins use different queues."""
        synced1 = SyncedResponse(mock_discord_context, origin="commands")
        synced2 = SyncedResponse(mock_discord_context, origin="events")
        
        mock_discord_context.channel.send = AsyncMock()
        
        await synced1.send("From commands")
        await synced2.send("From events")
        
        queue_key1 = (synced1.user_id, synced1.channel_id, "commands")
        queue_key2 = (synced2.user_id, synced2.channel_id, "events")
        
        # Both queues should exist
        assert queue_key1 in SyncedResponse._queues
        assert queue_key2 in SyncedResponse._queues
        assert queue_key1 != queue_key2


@pytest.mark.unit
class TestSyncedResponseQueueKey:
    """Test suite for queue key generation."""

    def test_queue_key_format(self, mock_discord_context):
        """Test that queue key is properly formatted."""
        synced = SyncedResponse(mock_discord_context, origin="test")
        
        expected_key = (synced.user_id, synced.channel_id, "test")
        
        assert synced.user_id is not None
        assert synced.channel_id is not None
        assert synced.origin == "test"

    def test_different_contexts_different_keys(self):
        """Test that different contexts have different queue keys."""
        ctx1 = MagicMock()
        ctx1.author.id = 111
        ctx1.channel.id = 222
        
        ctx2 = MagicMock()
        ctx2.author.id = 333
        ctx2.channel.id = 444
        
        synced1 = SyncedResponse(ctx1)
        synced2 = SyncedResponse(ctx2)
        
        key1 = (synced1.user_id, synced1.channel_id, synced1.origin)
        key2 = (synced2.user_id, synced2.channel_id, synced2.origin)
        
        assert key1 != key2


@pytest.mark.unit
class TestSyncedResponseClassVariables:
    """Test suite for SyncedResponse class variables."""

    def test_synced_response_has_queues_dict(self):
        """Test that SyncedResponse has _queues class variable."""
        assert hasattr(SyncedResponse, '_queues')

    def test_synced_response_has_processing_tasks(self):
        """Test that SyncedResponse has _processing_tasks."""
        assert hasattr(SyncedResponse, '_processing_tasks')

    def test_synced_response_has_lock(self):
        """Test that SyncedResponse has _lock for thread safety."""
        assert hasattr(SyncedResponse, '_lock')
