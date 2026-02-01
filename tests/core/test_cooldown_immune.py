"""Unit tests for core.CooldownImmune module."""

import pytest
from unittest.mock import MagicMock
from core.CooldownImmune import CooldownImmune


@pytest.mark.unit
class TestCooldownImmune:
    """Test suite for CooldownImmune class."""

    def test_cooldown_immune_initialization(self, mock_discord_context):
        """Test CooldownImmune initialization with context."""
        cooldown = CooldownImmune(mock_discord_context)
        
        assert cooldown.ctx == mock_discord_context
        assert cooldown.user_id == 0

    def test_cooldown_immune_initialization_with_user_id(self, mock_discord_context):
        """Test CooldownImmune initialization with user_id."""
        user_id = 123456789
        cooldown = CooldownImmune(mock_discord_context, user_id)
        
        assert cooldown.ctx == mock_discord_context
        assert cooldown.user_id == user_id

    def test_cooldown_immune_main_default_returns_true(self, mock_discord_context):
        """Test that main method returns True by default."""
        cooldown = CooldownImmune(mock_discord_context)
        result = cooldown.main()
        
        assert result is True

    def test_cooldown_immune_can_be_customized(self, mock_discord_context):
        """Test that CooldownImmune can be subclassed and customized."""
        class CustomCooldown(CooldownImmune):
            def main(self):
                if self.user_id in [123, 456]:
                    return True
                return False
        
        # User is in list
        cooldown1 = CustomCooldown(mock_discord_context, 123)
        assert cooldown1.main() is True
        
        # User is not in list
        cooldown2 = CustomCooldown(mock_discord_context, 789)
        assert cooldown2.main() is False

    def test_cooldown_immune_context_attribute(self, mock_discord_context):
        """Test that context is properly stored."""
        cooldown = CooldownImmune(mock_discord_context, 999)
        
        assert cooldown.ctx is not None
        assert cooldown.ctx.message is not None
        assert cooldown.ctx.author is not None

    def test_cooldown_immune_with_zero_user_id(self, mock_discord_context):
        """Test CooldownImmune with default user_id of 0."""
        cooldown = CooldownImmune(mock_discord_context, 0)
        
        assert cooldown.user_id == 0
        assert cooldown.main() is True

    def test_cooldown_immune_multiple_instances(self, mock_discord_context):
        """Test multiple CooldownImmune instances with different user IDs."""
        cooldown1 = CooldownImmune(mock_discord_context, 111)
        cooldown2 = CooldownImmune(mock_discord_context, 222)
        
        assert cooldown1.user_id == 111
        assert cooldown2.user_id == 222
        assert cooldown1.user_id != cooldown2.user_id
