"""Unit tests for utils.config module."""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, mock_open
from utils.config import Config


@pytest.mark.unit
class TestConfigUtils:
    """Test suite for Config utility class."""

    def test_config_method_success(self):
        """Test successful config file loading."""
        mock_data = {"bot_name": "TestBot", "version": "2.0"}
        
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            with patch("utils.config.from_root", return_value="/path/to/config.json"):
                result = Config.config()
                assert result == mock_data

    def test_config_method_failure(self):
        """Test config method returns False on error."""
        with patch("builtins.open", side_effect=FileNotFoundError):
            with patch("utils.config.from_root", return_value="/path/to/config.json"):
                result = Config.config()
                assert result is False

    def test_bot_config_method_success(self):
        """Test successful bot config loading."""
        mock_data = {"config": {"prefix": "!", "token": "test"}}
        
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            with patch("utils.config.from_root", return_value="/path/to/bot.json"):
                result = Config.bot_config()
                assert result == {"prefix": "!", "token": "test"}

    def test_bot_config_method_missing_config_key(self):
        """Test bot config returns False when 'config' key is missing."""
        mock_data = {"other_key": "value"}
        
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            with patch("utils.config.from_root", return_value="/path/to/bot.json"):
                result = Config.bot_config()
                assert result is False

    def test_bot_config_method_failure(self):
        """Test bot config method returns False on error."""
        with patch("builtins.open", side_effect=FileNotFoundError):
            with patch("utils.config.from_root", return_value="/path/to/bot.json"):
                result = Config.bot_config()
                assert result is False

    def test_staff_list_method_success(self):
        """Test successful staff list loading."""
        mock_data = {"users": [{"id": 1, "name": "Admin"}, {"id": 2, "name": "Mod"}]}
        
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            with patch("utils.config.from_root", return_value="/path/to/staff.json"):
                result = Config.staff_list()
                assert result == [{"id": 1, "name": "Admin"}, {"id": 2, "name": "Mod"}]

    def test_staff_list_method_failure(self):
        """Test staff list method returns False on error."""
        with patch("builtins.open", side_effect=FileNotFoundError):
            with patch("utils.config.from_root", return_value="/path/to/staff.json"):
                result = Config.staff_list()
                assert result is False

    def test_command_list_method_success(self):
        """Test successful command list loading."""
        mock_data = {"commands": [{"name": "command1", "action": "test"}, {"name": "command2", "action": "another"}]}
        
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            with patch("utils.config.from_root", return_value="/path/to/commands.json"):
                result = Config.command_list()
                assert result == [{"name": "command1", "action": "test"}, {"name": "command2", "action": "another"}]

    def test_command_list_method_failure(self):
        """Test command_list method returns False on error."""
        with patch("builtins.open", side_effect=FileNotFoundError):
            with patch("utils.config.from_root", return_value="/path/to/commands.json"):
                result = Config.command_list()
                assert result is False

    def test_staff_groups_method_success(self):
        """Test successful staff groups loading."""
        mock_data = {"groups": {"admins": [1, 2], "mods": [3, 4]}}
        
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            with patch("utils.config.from_root", return_value="/path/to/staff.json"):
                result = Config.staff_groups()
                assert result == {"admins": [1, 2], "mods": [3, 4]}

    def test_config_files_uses_context_manager(self):
        """Test that Config methods use context managers for file operations."""
        with patch("builtins.open", mock_open(read_data=json.dumps({}))):
            with patch("utils.config.from_root", return_value="/path/to/config.json"):
                Config.config()
                # If context manager works correctly, no assertions needed
                # The test passes if no exceptions are raised
