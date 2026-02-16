"""Unit tests for core.BaseDiscordEvent module."""

import pytest
from unittest.mock import MagicMock, AsyncMock
from core.BaseDiscordEvent import BaseDiscordEvent


@pytest.mark.unit
class TestBaseDiscordEvent:
    """Test suite for BaseDiscordEvent class."""

    def test_base_discord_event_initialization(self):
        """Test BaseDiscordEvent initialization with bot."""
        mock_bot = MagicMock()
        event = BaseDiscordEvent(mock_bot)

        assert event.bot == mock_bot

    def test_base_discord_event_has_event_name_attribute(self):
        """Test that BaseDiscordEvent has EVENT_NAME attribute."""
        assert hasattr(BaseDiscordEvent, "EVENT_NAME")
        assert BaseDiscordEvent.EVENT_NAME is None

    @pytest.mark.asyncio
    async def test_base_discord_event_main_raises_not_implemented(self):
        """Test that main method raises NotImplementedError."""
        mock_bot = MagicMock()
        event = BaseDiscordEvent(mock_bot)

        with pytest.raises(NotImplementedError):
            await event.main()

    @pytest.mark.asyncio
    async def test_custom_event_subclass_implementation(self):
        """Test that subclass can implement main method."""
        mock_bot = MagicMock()

        class CustomEvent(BaseDiscordEvent):
            EVENT_NAME = "on_test"

            async def main(self):
                return "custom_event_executed"

        event = CustomEvent(mock_bot)
        result = await event.main()

        assert result == "custom_event_executed"
        assert event.EVENT_NAME == "on_test"

    def test_custom_event_with_arguments(self):
        """Test custom event can receive arguments."""
        mock_bot = MagicMock()

        class CustomEvent(BaseDiscordEvent):
            EVENT_NAME = "on_message"

            async def main(self, message):
                self.message = message
                return message

        event = CustomEvent(mock_bot)
        assert event.bot == mock_bot
