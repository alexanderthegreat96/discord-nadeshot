"""Unit tests for factory.MessageFactory module."""

import pytest
from typing import Union, Dict
from factory.MessageFactory import MessageFactory


@pytest.mark.unit
class TestMessageFactory:
    """Test suite for MessageFactory class."""

    def test_message_factory_create_direct_message_basic(self):
        """Test creating a direct message."""
        user_id = 123456789
        content = "Hello, user!"
        
        message = MessageFactory.create_direct_message(user_id, content)
        
        assert isinstance(message, dict)
        assert message.get("message_type") == "direct_message"
        assert message.get("user_id") == user_id
        assert message.get("to_send") == content
        assert message.get("server_id") == 0
        assert message.get("channel_id") == 0

    def test_message_factory_create_direct_message_without_content(self):
        """Test creating a direct message without content."""
        user_id = 123456789
        
        message = MessageFactory.create_direct_message(user_id)
        
        assert message.get("message_type") == "direct_message"
        assert message.get("user_id") == user_id
        assert message.get("to_send") is None

    def test_message_factory_create_direct_message_with_dict(self):
        """Test creating a direct message with dict content (embed)."""
        user_id = 123456789
        embed_dict = {"title": "Embed", "description": "Test"}
        
        message = MessageFactory.create_direct_message(user_id, embed_dict)
        
        assert message.get("to_send") == embed_dict

    def test_message_factory_create_regular_message(self):
        """Test creating a regular server message."""
        server_id = 987654321
        channel_id = 555555555
        content = "Hello, channel!"
        
        message = MessageFactory.create_regular_message(server_id, channel_id, content)
        
        assert isinstance(message, dict)
        assert message.get("message_type") == "regular_message"
        assert message.get("server_id") == server_id
        assert message.get("channel_id") == channel_id
        assert message.get("to_send") == content

    def test_message_factory_create_regular_message_with_user_id(self):
        """Test creating a regular message with user_id."""
        server_id = 987654321
        channel_id = 555555555
        user_id = 123456789
        
        message = MessageFactory.create_regular_message(
            server_id, channel_id, user_id=user_id
        )
        
        assert message.get("user_id") == user_id

    def test_message_factory_create_regular_message_without_content(self):
        """Test creating a regular message without content."""
        server_id = 987654321
        channel_id = 555555555
        
        message = MessageFactory.create_regular_message(server_id, channel_id)
        
        assert message.get("to_send") is None
        assert message.get("server_id") == server_id
        assert message.get("channel_id") == channel_id

    def test_message_factory_create_regular_message_with_dict(self):
        """Test creating a regular message with dict content."""
        server_id = 987654321
        channel_id = 555555555
        embed_dict = {"title": "Test", "color": 0xFF0000}
        
        message = MessageFactory.create_regular_message(
            server_id, channel_id, embed_dict
        )
        
        assert message.get("to_send") == embed_dict

    def test_message_factory_message_structure(self):
        """Test that messages have required structure."""
        message = MessageFactory.create_direct_message(123, "test")
        
        required_keys = ["message_type", "user_id", "to_send"]
        for key in required_keys:
            assert key in message

    def test_message_factory_multiple_messages_independent(self):
        """Test that multiple messages are independent."""
        msg1 = MessageFactory.create_direct_message(111, "msg1")
        msg2 = MessageFactory.create_direct_message(222, "msg2")
        
        assert msg1.get("user_id") != msg2.get("user_id")
        assert msg1.get("to_send") != msg2.get("to_send")

    def test_message_factory_create_custom_message(self):
        """Test creating a custom message type."""
        custom_message = MessageFactory.create_custom_message(
            "custom_type",
            user_id=999,
            to_send="custom content"
        )
        
        assert custom_message.get("message_type") == "custom_type"
        assert custom_message.get("to_send") == "custom content"
        assert custom_message.get("user_id") == 999
