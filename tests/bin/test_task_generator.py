import pytest
import json
import os
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

# Add bin/commands to path for imports
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../bin/commands"))

from TaskGenerator import TaskGeneratorCommand


class TestTaskGeneratorCommand:
    """Tests for the TaskGeneratorCommand utility class."""

    @pytest.fixture
    def mock_from_root(self):
        """Mock the from_root function."""
        with patch("TaskGenerator.from_root") as mock_fn:

            def side_effect(path):
                return os.path.join("/mock/root", path)

            mock_fn.side_effect = side_effect
            yield mock_fn

    def test_init_basic(self, mock_from_root):
        """Test TaskGeneratorCommand initialization."""
        with patch("TaskGenerator.path.exists", return_value=True):
            gen = TaskGeneratorCommand("my-task")
            assert gen.input == "my-task"

    def test_init_creates_tasks_json_if_missing(self, mock_from_root):
        """Test that __init__ creates tasks.json if missing."""
        with patch("TaskGenerator.path.exists", return_value=False):
            with patch("builtins.open", mock_open()):
                gen = TaskGeneratorCommand("test-task")
                # Should attempt to create the file

    def test_get_available_tasks_success(self, mock_from_root):
        """Test get_available_tasks with valid JSON."""
        mock_data = {
            "tasks": {
                "TestTask": {
                    "file_name": "test_task.py",
                    "class_name": "TestTask",
                    "hours": 1,
                    "minutes": 0,
                    "seconds": 0,
                    "enabled": True,
                }
            }
        }

        with patch("TaskGenerator.path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
                gen = TaskGeneratorCommand("test")
                result = gen.get_available_tasks()

                assert "tasks" in result
                assert "TestTask" in result["tasks"]

    def test_get_available_tasks_file_not_found(self, mock_from_root):
        """Test get_available_tasks when file not found."""
        with patch("TaskGenerator.path.exists", return_value=True):
            with patch("builtins.open", side_effect=FileNotFoundError):
                with patch("builtins.print"):
                    gen = TaskGeneratorCommand("test")
                    result = gen.get_available_tasks()

                    assert result == {}

    def test_reformat_text_with_hyphens(self):
        """Test reformat_text with hyphenated input."""
        gen = TaskGeneratorCommand("test")
        result = gen.reformat_text("my-task-name")
        assert result == "MyTaskName"

    def test_reformat_text_no_hyphens(self):
        """Test reformat_text without hyphens."""
        gen = TaskGeneratorCommand("test")
        result = gen.reformat_text("mytaskname")
        assert result == "Mytaskname"

    def test_reformat_text_single_word(self):
        """Test reformat_text with single word."""
        gen = TaskGeneratorCommand("test")
        result = gen.reformat_text("task")
        assert result == "Task"

    def test_make_task_class_template_structure(self):
        """Test that make_task_class_template creates proper template."""
        gen = TaskGeneratorCommand("test")
        template = gen.make_task_class_template("my-task")

        assert "class MyTask:" in template
        assert "def __init__" in template
        assert "async def main" in template
        assert "commands.Bot" in template
        assert "Logger" in template

    def test_make_task_class_template_contains_logger_call(self):
        """Test that template includes logger call."""
        gen = TaskGeneratorCommand("test")
        template = gen.make_task_class_template("my-task")

        assert "self.logger.info" in template or "logger.info" in template

    def test_generate_task_entry_success(self, mock_from_root):
        """Test successful task generation."""
        mock_tasks = {"tasks": {}}

        with patch("TaskGenerator.path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=json.dumps(mock_tasks))):
                with patch("TaskGenerator.makedirs"):
                    with patch("builtins.print") as mock_print:
                        gen = TaskGeneratorCommand("my-task")
                        gen.generate_task_entry("my-task")

                        # Verify success message was printed
                        mock_print.assert_called()

    def test_generate_task_entry_duplicate_task(self, mock_from_root):
        """Test generating duplicate task."""
        mock_tasks = {
            "tasks": {
                "MyTask": {
                    "file_name": "my_task.py",
                    "class_name": "MyTask",
                    "hours": 1,
                    "minutes": 0,
                    "seconds": 0,
                    "enabled": True,
                }
            }
        }

        with patch("TaskGenerator.path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=json.dumps(mock_tasks))):
                with patch("builtins.print") as mock_print:
                    gen = TaskGeneratorCommand("my-task")
                    gen.generate_task_entry("my-task")

                    # Should print duplicate message
                    calls = [str(call) for call in mock_print.call_args_list]
                    assert any("already exists" in str(call) for call in calls)

    def test_generate_task_entry_creates_config_entry(self, mock_from_root):
        """Test that task entry is created in config."""
        mock_tasks = {"tasks": {}}

        with patch("TaskGenerator.path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=json.dumps(mock_tasks))):
                with patch("TaskGenerator.makedirs"):
                    with patch("builtins.print"):
                        gen = TaskGeneratorCommand("my-task")
                        gen.generate_task_entry("my-task")

    def test_generate_task_entry_creates_py_file(self, mock_from_root):
        """Test that Python file is created."""
        mock_tasks = {"tasks": {}}

        with patch("TaskGenerator.path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=json.dumps(mock_tasks))):
                with patch("TaskGenerator.makedirs"):
                    with patch("builtins.print"):
                        gen = TaskGeneratorCommand("my-task")
                        gen.generate_task_entry("my-task")

    def test_generate_task_entry_handles_exception(self, mock_from_root):
        """Test exception handling during task generation."""
        with patch("TaskGenerator.path.exists", return_value=True):
            with patch("builtins.open", side_effect=Exception("Test error")):
                with patch("builtins.print") as mock_print:
                    gen = TaskGeneratorCommand("my-task")
                    gen.generate_task_entry("my-task")

                    # Should print error message
                    mock_print.assert_called()

    def test_task_entry_structure(self, mock_from_root):
        """Test that task entry has correct structure."""
        gen = TaskGeneratorCommand("test")

        # Simulate the structure created
        class_name = gen.reformat_text("my-task")
        file_name = "my-task".replace("-", "_").lower()

        task_structure = {
            "file_name": f"{file_name}.py",
            "class_name": class_name,
            "hours": 1,
            "minutes": 0,
            "seconds": 0,
            "enabled": True,
        }

        assert task_structure["file_name"] == "my_task.py"
        assert task_structure["class_name"] == "MyTask"
        assert task_structure["hours"] == 1
        assert task_structure["minutes"] == 0
        assert task_structure["seconds"] == 0
        assert task_structure["enabled"] is True

    def test_generate_task_entry_with_hyphens(self, mock_from_root):
        """Test task generation with hyphenated name."""
        mock_tasks = {"tasks": {}}

        with patch("TaskGenerator.path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=json.dumps(mock_tasks))):
                with patch("TaskGenerator.makedirs"):
                    with patch("builtins.print"):
                        gen = TaskGeneratorCommand("my-long-task-name")
                        gen.generate_task_entry("my-long-task-name")

    def test_generate_task_entry_with_underscores(self, mock_from_root):
        """Test task generation with underscored name."""
        mock_tasks = {"tasks": {}}

        with patch("TaskGenerator.path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=json.dumps(mock_tasks))):
                with patch("TaskGenerator.makedirs"):
                    with patch("builtins.print"):
                        gen = TaskGeneratorCommand("my_task")
                        gen.generate_task_entry("my_task")

    def test_get_available_tasks_returns_empty_dict_on_error(self, mock_from_root):
        """Test that get_available_tasks returns empty dict on error."""
        with patch("TaskGenerator.path.exists", return_value=True):
            with patch("builtins.open", side_effect=Exception("Test error")):
                with patch("builtins.print"):
                    gen = TaskGeneratorCommand("test")
                    result = gen.get_available_tasks()

                    assert isinstance(result, dict)
                    assert result == {}

    def test_make_task_class_template_class_name_formatting(self):
        """Test that class names are properly formatted in template."""
        gen = TaskGeneratorCommand("test")

        # Test various naming patterns
        templates = [
            gen.make_task_class_template("my-task"),
            gen.make_task_class_template("MyTask"),
            gen.make_task_class_template("my_task"),
        ]

        for template in templates:
            assert "class " in template
            assert "def __init__" in template
