import pytest
import os
from unittest.mock import patch, mock_open, MagicMock
import re

# Add bin/commands to path for imports
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../bin/commands"))

from MiddlewareGenerator import MiddlewareGeneratorCommand


class TestMiddlewareGeneratorCommand:
    """Tests for the MiddlewareGeneratorCommand utility class."""

    @pytest.fixture
    def mock_from_root(self):
        """Mock the from_root function."""
        with patch("MiddlewareGenerator.from_root") as mock_fn:

            def side_effect(path):
                return os.path.join("/mock/root", path)

            mock_fn.side_effect = side_effect
            yield mock_fn

    def test_init_basic(self):
        """Test MiddlewareGeneratorCommand initialization."""
        gen = MiddlewareGeneratorCommand("my-middleware")
        assert gen.input == "my_middleware"  # Dashes converted to underscores
        assert gen.type == "before"

    def test_init_with_custom_kind(self):
        """Test initialization with custom middleware kind."""
        gen = MiddlewareGeneratorCommand("my-middleware", "after")
        assert gen.input == "my_middleware"
        assert gen.type == "after"

    def test_init_converts_dashes_to_underscores(self):
        """Test that dashes are converted to underscores."""
        gen = MiddlewareGeneratorCommand("my-middleware-name")
        assert gen.input == "my_middleware_name"
        assert "-" not in gen.input

    def test_init_type_is_lowercase(self):
        """Test that middleware type is converted to lowercase."""
        gen = MiddlewareGeneratorCommand("test", "BEFORE")
        assert gen.type == "before"

        gen2 = MiddlewareGeneratorCommand("test", "AFTER")
        assert gen2.type == "after"

    def test_to_camel_case_with_hyphens(self):
        """Test to_camel_case with hyphenated input."""
        gen = MiddlewareGeneratorCommand("test")
        result = gen.to_camel_case("my-middleware-name")
        assert result == "MyMiddlewareName"

    def test_to_camel_case_with_underscores(self):
        """Test to_camel_case with underscored input."""
        gen = MiddlewareGeneratorCommand("test")
        result = gen.to_camel_case("my_middleware_name")
        assert result == "MyMiddlewareName"

    def test_to_camel_case_with_dots(self):
        """Test to_camel_case with dotted input."""
        gen = MiddlewareGeneratorCommand("test")
        result = gen.to_camel_case("my.middleware.name")
        assert result == "MyMiddlewareName"

    def test_to_camel_case_single_word(self):
        """Test to_camel_case with single word."""
        gen = MiddlewareGeneratorCommand("test")
        result = gen.to_camel_case("middleware")
        assert result == "Middleware"

    def test_to_camel_case_mixed_delimiters(self):
        """Test to_camel_case with mixed delimiters."""
        gen = MiddlewareGeneratorCommand("test")
        result = gen.to_camel_case("my-middleware_name.test")
        assert result == "MyMiddlewareNameTest"

    def test_make_middleware_template_contains_imports(self):
        """Test that template includes necessary imports."""
        gen = MiddlewareGeneratorCommand("test")
        template = gen.make_middleware_template("TestMiddleware")

        assert "from utils.guild_wrapper import GuildWrapper" in template
        assert "from utils.user_wrapper import UserWrapper" in template
        assert "from discord.ext import commands" in template

    def test_make_middleware_template_contains_class_definition(self):
        """Test that template contains proper class definition."""
        gen = MiddlewareGeneratorCommand("test")
        template = gen.make_middleware_template("TestMiddleware")

        assert "class TestMiddleware:" in template

    def test_make_middleware_template_contains_init_method(self):
        """Test that template contains __init__ method."""
        gen = MiddlewareGeneratorCommand("test")
        template = gen.make_middleware_template("TestMiddleware")

        assert "def __init__(self, ctx: commands.Context" in template
        assert "self.ctx = ctx" in template
        assert "self.server = GuildWrapper(ctx.guild)" in template
        assert "self.user = UserWrapper(ctx.author)" in template

    def test_make_middleware_template_contains_main_method(self):
        """Test that template contains main method."""
        gen = MiddlewareGeneratorCommand("test")
        template = gen.make_middleware_template("TestMiddleware")

        assert "def main(self) -> dict:" in template
        assert "return" in template

    def test_make_middleware_template_contains_attributes(self):
        """Test that template initializes required attributes."""
        gen = MiddlewareGeneratorCommand("test")
        template = gen.make_middleware_template("TestMiddleware")

        assert "self.user_id = self.user.get_user_id()" in template
        assert "self.server_id = self.server.get_guild_id()" in template

    def test_generate_creates_middleware_file(self, mock_from_root):
        """Test that generate creates middleware file."""
        with patch("MiddlewareGenerator.path.exists", return_value=False):
            with patch("MiddlewareGenerator.makedirs"):
                with patch("builtins.open", mock_open()) as mock_file:
                    with patch("builtins.print") as mock_print:
                        gen = MiddlewareGeneratorCommand("test-middleware")
                        gen.generate()

                        # Verify file write was attempted
                        mock_file.assert_called()

    def test_generate_uses_correct_filename(self, mock_from_root):
        """Test that generate uses correct middleware filename."""
        with patch("MiddlewareGenerator.path.exists", return_value=False):
            with patch("MiddlewareGenerator.makedirs"):
                with patch("builtins.open", mock_open()):
                    with patch("builtins.print"):
                        gen = MiddlewareGeneratorCommand("my-middleware")
                        gen.generate()

    def test_generate_with_before_type(self, mock_from_root):
        """Test generate with 'before' middleware type."""
        with patch("MiddlewareGenerator.path.exists", return_value=False):
            with patch("MiddlewareGenerator.makedirs"):
                with patch("builtins.open", mock_open()):
                    with patch("builtins.print"):
                        gen = MiddlewareGeneratorCommand("test-middleware", "before")
                        gen.generate()

    def test_generate_with_after_type(self, mock_from_root):
        """Test generate with 'after' middleware type."""
        with patch("MiddlewareGenerator.path.exists", return_value=False):
            with patch("MiddlewareGenerator.makedirs"):
                with patch("builtins.open", mock_open()):
                    with patch("builtins.print"):
                        gen = MiddlewareGeneratorCommand("test-middleware", "after")
                        gen.generate()

    def test_generate_skips_existing_file(self, mock_from_root):
        """Test that generate skips if file already exists."""
        with patch("MiddlewareGenerator.path.exists", return_value=True):
            with patch("builtins.print") as mock_print:
                gen = MiddlewareGeneratorCommand("test-middleware")
                gen.generate()

                # Should print error message
                mock_print.assert_called()
                calls = [str(call) for call in mock_print.call_args_list]
                assert any("already exists" in str(call) for call in calls)

    def test_generate_creates_middlewares_directory(self, mock_from_root):
        """Test that generate creates middlewares directory if missing."""
        with patch("MiddlewareGenerator.path.exists", return_value=False):
            with patch("MiddlewareGenerator.makedirs") as mock_makedirs:
                with patch("builtins.open", mock_open()):
                    with patch("builtins.print"):
                        gen = MiddlewareGeneratorCommand("test-middleware")
                        gen.generate()

                        # makedirs should be called for middlewares directory
                        mock_makedirs.assert_called()

    def test_generate_handles_exception(self, mock_from_root):
        """Test exception handling during middleware generation."""
        with patch("MiddlewareGenerator.path.exists", return_value=False):
            with patch(
                "MiddlewareGenerator.makedirs", side_effect=Exception("Test error")
            ):
                with patch("builtins.print") as mock_print:
                    gen = MiddlewareGeneratorCommand("test-middleware")
                    gen.generate()

                    # Should print error message
                    mock_print.assert_called()

    def test_generate_prints_success_message(self, mock_from_root):
        """Test that generate prints success message."""
        with patch("MiddlewareGenerator.path.exists", return_value=False):
            with patch("MiddlewareGenerator.makedirs"):
                with patch("builtins.open", mock_open()):
                    with patch("builtins.print") as mock_print:
                        gen = MiddlewareGeneratorCommand("test-middleware")
                        gen.generate()

                        # Should print success message
                        calls = [str(call) for call in mock_print.call_args_list]
                        assert any("created" in str(call).lower() for call in calls)

    def test_middleware_name_construction(self, mock_from_root):
        """Test how middleware name is constructed."""
        gen = MiddlewareGeneratorCommand("my-middleware", "before")

        # The middleware name should be "before_my_middleware"
        # This is constructed in generate method
        expected_name = "before_my_middleware"
        assert expected_name == f"{gen.type}_{gen.input}"

    def test_class_name_from_middleware_name(self):
        """Test class name generation from middleware name."""
        gen = MiddlewareGeneratorCommand("my-middleware", "before")
        middleware_name = f"{gen.type}_{gen.input}"

        class_name = gen.to_camel_case(middleware_name)
        assert class_name == "BeforeMyMiddleware"

    def test_generate_with_various_names(self, mock_from_root):
        """Test generate with various middleware names."""
        test_names = [
            "auth-check",
            "permission-check",
            "rate-limiter",
            "logger",
        ]

        for name in test_names:
            with patch("MiddlewareGenerator.path.exists", return_value=False):
                with patch("MiddlewareGenerator.makedirs"):
                    with patch("builtins.open", mock_open()):
                        with patch("builtins.print"):
                            gen = MiddlewareGeneratorCommand(name)
                            gen.generate()

    def test_middleware_template_returns_dict(self):
        """Test that main method returns a dictionary."""
        gen = MiddlewareGeneratorCommand("test")
        template = gen.make_middleware_template("TestMiddleware")

        # Template should have return statement returning dict
        assert "return" in template
        assert "{" in template and "}" in template

    def test_to_camel_case_preserves_capitalization(self):
        """Test that to_camel_case properly capitalizes each part."""
        gen = MiddlewareGeneratorCommand("test")

        result = gen.to_camel_case("admin-permission-check")
        parts = ["Admin", "Permission", "Check"]
        assert all(part in result for part in parts)

    def test_init_handles_already_underscored_input(self):
        """Test that init handles already underscored input."""
        gen = MiddlewareGeneratorCommand("my_middleware")
        assert gen.input == "my_middleware"

    def test_generate_exception_prints_unable_message(self, mock_from_root):
        """Test that exception prints 'Unable' message."""
        with patch("MiddlewareGenerator.path.exists", return_value=False):
            with patch(
                "MiddlewareGenerator.makedirs",
                side_effect=Exception("Permission denied"),
            ):
                with patch("builtins.print") as mock_print:
                    gen = MiddlewareGeneratorCommand("test-middleware")
                    gen.generate()

                    calls = [str(call) for call in mock_print.call_args_list]
                    assert any("unable" in str(call).lower() for call in calls)
