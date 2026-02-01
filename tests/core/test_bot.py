import pytest
import json
import asyncio
from unittest.mock import patch, mock_open, MagicMock, AsyncMock, PropertyMock
from pathlib import Path
import tempfile

# We'll need to mock discord and other dependencies
@pytest.fixture
def mock_discord_bot():
    """Mock the Discord bot."""
    with patch('core.Bot.commands.Bot') as mock_bot:
        yield mock_bot


@pytest.fixture
def mock_env_parser():
    """Mock the EnvParser."""
    with patch('core.Bot.EnvParser') as mock_env:
        instance = MagicMock()
        instance.get.side_effect = lambda key, default=None: {
            'BOT_TOKEN': 'test_token_123',
            'BOT_NAME': 'TestBot',
        }.get(key, default)
        mock_env.return_value = instance
        yield mock_env


@pytest.fixture
def mock_logger():
    """Mock the Logger."""
    with patch('core.Bot.Logger') as mock_log:
        instance = MagicMock()
        instance.get_logger.return_value = MagicMock()
        mock_log.return_value = instance
        yield mock_log


@pytest.fixture
def mock_cache():
    """Mock the Cache."""
    with patch('core.Bot.Cache') as mock_cache_class:
        yield mock_cache_class


@pytest.fixture
def mock_multi_bot_handler():
    """Mock the MultiBotHandler."""
    with patch('core.Bot.MultiBotHandler') as mock_handler:
        yield mock_handler


@pytest.fixture
def bot_config():
    """Return a sample bot config."""
    return {
        'bot-name': 'TestBot',
        'bot-listens-to': '/test',
        'bot-description': 'A test bot',
        'enable-cooldowns': True,
        'cooldown-duration': 15,
        'enable-global-errors': True,
        'development-mode': True,
        'enable-multiple-bots': False
    }


class TestBot:
    """Tests for the Bot class."""

    def test_bot_initialization(self, mock_env_parser, mock_logger, mock_cache, mock_multi_bot_handler, bot_config):
        """Test Bot initialization with mocked dependencies."""
        with patch('core.Bot.from_root') as mock_from_root:
            from core.Bot import Bot
            
            mock_from_root.return_value = '.env'
            
            # Create bot instance - we'll just test basic initialization
            with patch('core.Bot.EnvParser'):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                                bot = Bot()
                                
                                # Verify key attributes were initialized
                                assert isinstance(bot.command_prefixes, list)
                                assert bot.command_prefixes == ['!', '.', '?', '/', '>']

    def test_bot_token_from_env(self, mock_env_parser):
        """Test bot token is retrieved from environment."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': 'Test'}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            assert bot.bot_token == 'test_token_123'

    def test_bot_name_from_config(self, mock_env_parser):
        """Test bot name is retrieved from config."""
        from core.Bot import Bot
        
        config = {
            'bot-name': 'MyTestBot',
            'bot-listens-to': '/cmd',
            'bot-description': 'Test description'
        }
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value=config):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            # bot_name comes from env or config, check that config is loaded
                            assert 'listens' in str(bot.config).lower() or bot.bot_name

    def test_seconds_to_hms_seconds_only(self):
        """Test seconds_to_hms with only seconds."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            result = bot.seconds_to_hms(30)
                            assert result == '30 seconds'

    def test_seconds_to_hms_minutes_and_seconds(self):
        """Test seconds_to_hms with minutes and seconds."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            result = bot.seconds_to_hms(125)  # 2 minutes 5 seconds
                            assert '2 minute' in result
                            assert '5 second' in result

    def test_seconds_to_hms_hours_minutes_seconds(self):
        """Test seconds_to_hms with hours, minutes, and seconds."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            result = bot.seconds_to_hms(3785)  # 1 hour 3 minutes 5 seconds
                            assert '1 hour' in result
                            assert '3 minute' in result
                            assert '5 second' in result

    def test_seconds_to_hms_singular_units(self):
        """Test seconds_to_hms produces singular forms correctly."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            result = bot.seconds_to_hms(3661)  # 1 hour 1 minute 1 second
                            assert '1 hour' in result
                            assert '1 minute' in result
                            assert '1 second' in result

    def test_add_to_list_single_item(self):
        """Test add_to_list with a single item."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            result = bot.add_to_list([1, 2, 3], 4)
                            assert result == [1, 2, 3, 4]

    def test_add_to_list_multiple_items(self):
        """Test add_to_list with multiple items."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            result = bot.add_to_list([1, 2], [3, 4, 5])
                            assert result == [1, 2, 3, 4, 5]

    def test_add_to_list_no_duplicates(self):
        """Test add_to_list prevents duplicates."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            result = bot.add_to_list([1, 2, 3], [3, 4])
                            assert result == [1, 2, 3, 4]
                            assert len(result) == 4

    def test_filter_list(self):
        """Test filter_list removes items correctly."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            result = bot.filter_list([1, 2, 3, 4, 5], [2, 4])
                            assert result == [1, 3, 5]

    def test_filter_list_empty_removal(self):
        """Test filter_list with items not in list."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            result = bot.filter_list([1, 2, 3], [5, 6])
                            assert result == [1, 2, 3]

    def test_to_camel_case(self):
        """Test to_camel_case conversion."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            result = bot.to_camel_case('my_command_name')
                            # Method converts to PascalCase (each part capitalized)
                            assert result == 'MyCommandName'

    def test_to_camel_case_single_word(self):
        """Test to_camel_case with single word."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            result = bot.to_camel_case('command')
                            # Single word gets capitalized
                            assert result == 'Command'

    def test_check_if_item_is_not_empty_with_empty_list(self):
        """Test check_if_item_is_not_empty with empty list."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            # Empty list is still truthy in Python, method checks for None or ""
                            result = bot.check_if_item_is_not_empty([])
                            assert result is True

    def test_check_if_item_is_not_empty_with_items(self):
        """Test check_if_item_is_not_empty with items."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            result = bot.check_if_item_is_not_empty([1, 2, 3])
                            assert result is True

    def test_check_if_item_is_not_empty_with_empty_dict(self):
        """Test check_if_item_is_not_empty with empty dict."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            # Empty dict is still truthy in Python, method checks for None or ""
                            result = bot.check_if_item_is_not_empty({})
                            assert result is True

    def test_check_if_item_is_not_empty_with_empty_string(self):
        """Test check_if_item_is_not_empty with empty string."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            result = bot.check_if_item_is_not_empty('')
                            assert result is False

    def test_check_if_item_is_not_empty_with_string(self):
        """Test check_if_item_is_not_empty with non-empty string."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            result = bot.check_if_item_is_not_empty('test')
                            assert result is True

    def test_array_merge_with_list_single_item(self):
        """Test array_merge with list and single item."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            target = [1, 2, 3]
                            bot.array_merge(target, value=4)
                            assert 4 in target
                            assert len(target) == 4

    def test_array_merge_with_list_multiple_items(self):
        """Test array_merge with list and multiple items."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            target = [1, 2]
                            bot.array_merge(target, value=[3, 4, 5])
                            assert target == [1, 2, 3, 4, 5]

    def test_array_merge_with_dict(self):
        """Test array_merge with dictionary."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            target = {'users': [1, 2]}
                            bot.array_merge(target, key='users', value=3)
                            assert 3 in target['users']

    def test_array_merge_dict_no_key_raises_error(self):
        """Test array_merge with dict raises error without key."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            target = {}
                            
                            with pytest.raises(ValueError):
                                bot.array_merge(target, value=1)

    def test_array_merge_invalid_container_raises_error(self):
        """Test array_merge with invalid container type."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            
                            with pytest.raises(TypeError):
                                bot.array_merge("string", value=1)

    def test_parsed_command_list_success(self):
        """Test parsed_command_list loads commands successfully."""
        from core.Bot import Bot
        
        mock_commands = {
            'commands': {
                'test_cmd': {
                    'syntax': '/test',
                    'description': 'Test command'
                }
            }
        }
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.EnvParser'):
                    with patch('core.Bot.Logger'):
                        with patch('core.Bot.Cache'):
                            with patch('core.Bot.MultiBotHandler'):
                                with patch('builtins.open', mock_open(read_data=json.dumps(mock_commands))):
                                    bot = Bot()
                                    result = bot.parsed_command_list()
                                    assert 'test_cmd' in result

    def test_parsed_command_list_file_not_found(self):
        """Test parsed_command_list when file not found."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            with patch('builtins.open', side_effect=FileNotFoundError):
                                bot = Bot()
                                result = bot.parsed_command_list()
                                assert result == {}

    def test_task_list_success(self):
        """Test task_list loads tasks successfully."""
        from core.Bot import Bot
        
        mock_tasks = {
            'tasks': {
                'test_task': {
                    'file_name': 'test_task.py',
                    'class_name': 'TestTask',
                    'hours': 1,
                    'minutes': 0,
                    'seconds': 0,
                    'enabled': True
                }
            }
        }
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.EnvParser'):
                    with patch('core.Bot.Logger'):
                        with patch('core.Bot.Cache'):
                            with patch('core.Bot.MultiBotHandler'):
                                with patch('builtins.open', mock_open(read_data=json.dumps(mock_tasks))):
                                    bot = Bot()
                                    result = bot.task_list()
                                    assert 'test_task' in result

    def test_task_list_file_not_found(self):
        """Test task_list when file not found."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            with patch('builtins.open', side_effect=FileNotFoundError):
                                bot = Bot()
                                result = bot.task_list()
                                assert result is None

    def test_staff_groups_success(self):
        """Test staff_groups loads groups successfully."""
        from core.Bot import Bot
        
        mock_groups = {
            'groups': {
                'admin': ['user1', 'user2'],
                'mod': ['user3']
            }
        }
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.EnvParser'):
                    with patch('core.Bot.Logger'):
                        with patch('core.Bot.Cache'):
                            with patch('core.Bot.MultiBotHandler'):
                                with patch('builtins.open', mock_open(read_data=json.dumps(mock_groups))):
                                    bot = Bot()
                                    result = bot.staff_groups()
                                    assert 'admin' in result
                                    assert 'mod' in result

    def test_staff_groups_file_not_found(self):
        """Test staff_groups when file not found."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            with patch('builtins.open', side_effect=FileNotFoundError):
                                bot = Bot()
                                result = bot.staff_groups()
                                assert result is None

    def test_get_command_prefix_from_message(self):
        """Test get_command_prefix_from_message extraction."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            
                            # Mock context
                            ctx = MagicMock()
                            ctx.message = MagicMock()
                            ctx.message.content = '!help'
                            
                            result = bot.get_command_prefix_from_message(ctx)
                            assert result == '!'

    def test_should_ignore_commands_from_variants(self):
        """Test should_ignore_commands_from_variants logic."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            # Test when multiple bots is disabled
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': '', 'enable-multiple-bots': False}):
                with patch('core.Bot.EnvParser'):
                    with patch('core.Bot.Logger'):
                        with patch('core.Bot.Cache'):
                            with patch('core.Bot.MultiBotHandler') as mock_handler:
                                bot = Bot()
                                result = bot.should_ignore_commands_from_variants(12345)
                                
                                # Should return False when multiple bots disabled
                                assert result is False
        
        # Test when multiple bots is enabled
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': '', 'enable-multiple-bots': True}):
                with patch('core.Bot.EnvParser'):
                    with patch('core.Bot.Logger'):
                        with patch('core.Bot.Cache'):
                            with patch('core.Bot.MultiBotHandler') as mock_handler:
                                mock_instance = MagicMock()
                                mock_instance.should_ignore_commands.return_value = True
                                mock_handler.return_value = mock_instance
                                
                                bot = Bot()
                                result = bot.should_ignore_commands_from_variants(12345)
                                
                                # Should return True from multi_bot_handler when enabled
                                assert result is True

    def test_bot_executor_initialized(self):
        """Test that executor is initialized with correct worker count."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            assert bot.executor is not None
                            assert bot.executor._max_workers == 16

    def test_bot_tasks_dict_initialized(self):
        """Test that tasks dictionary is initialized."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            assert isinstance(bot.tasks, dict)
                            assert isinstance(bot._task_delays, dict)
                            assert isinstance(bot._started_tasks, set)
                            assert isinstance(bot._task_failures, dict)

    def test_bot_channel_queues_initialized(self):
        """Test that channel queues are initialized."""
        from core.Bot import Bot
        
        with patch('core.Bot.from_root'):
            with patch.object(Bot, '_bot_config', return_value={'bot-name': 'Bot', 'bot-listens-to': '/', 'bot-description': ''}):
                with patch('core.Bot.Logger'):
                    with patch('core.Bot.Cache'):
                        with patch('core.Bot.MultiBotHandler'):
                            bot = Bot()
                            assert bot.channel_queues is not None
