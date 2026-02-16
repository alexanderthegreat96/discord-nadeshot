"""Unit tests for core.EnvParser module."""

import pytest
import os
import tempfile
from pathlib import Path
from core.EnvParser import EnvParser


@pytest.mark.unit
class TestEnvParserInitialization:
    """Test suite for EnvParser initialization."""

    def test_env_parser_initialization_with_valid_file(self):
        """Test EnvParser initialization with valid .env file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("TEST_VAR=test_value\n")
            f.write("TEST_NUMBER=42\n")
            f.flush()
            temp_path = f.name

        try:
            parser = EnvParser(temp_path)
            assert parser is not None
        finally:
            os.unlink(temp_path)

    def test_env_parser_initialization_with_nonexistent_file(self):
        """Test EnvParser with non-existent file."""
        parser = EnvParser("/nonexistent/path/.env")
        assert parser.get_error() is not None

    def test_env_parser_get_error_returns_none_on_success(self):
        """Test that get_error returns None on successful parsing."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("VALID=value\n")
            f.flush()
            temp_path = f.name

        try:
            parser = EnvParser(temp_path)
            error = parser.get_error()
            assert error is None
        finally:
            os.unlink(temp_path)

    def test_env_parser_parse_string_value(self):
        """Test parsing string environment variables."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("STRING_VAR=hello_world\n")
            f.flush()
            temp_path = f.name

        try:
            parser = EnvParser(temp_path)
            value = parser.get("STRING_VAR", "str")
            assert value == "hello_world"
        finally:
            os.unlink(temp_path)

    def test_env_parser_parse_int_value(self):
        """Test parsing integer environment variables."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("INT_VAR=123\n")
            f.flush()
            temp_path = f.name

        try:
            parser = EnvParser(temp_path)
            value = parser.get("INT_VAR", "int")
            assert value == 123
            assert isinstance(value, int)
        finally:
            os.unlink(temp_path)

    def test_env_parser_parse_bool_true(self):
        """Test parsing boolean true values."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("BOOL_VAR=True\n")
            f.flush()
            temp_path = f.name

        try:
            parser = EnvParser(temp_path)
            value = parser.get("BOOL_VAR", "bool")
            assert value is True
        finally:
            os.unlink(temp_path)

    def test_env_parser_parse_bool_false(self):
        """Test parsing boolean false values."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("BOOL_VAR=False\n")
            f.flush()
            temp_path = f.name

        try:
            parser = EnvParser(temp_path)
            value = parser.get("BOOL_VAR", "bool")
            assert value is False
        finally:
            os.unlink(temp_path)

    def test_env_parser_default_value_when_key_missing(self):
        """Test that default value is returned when key is missing."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("OTHER_VAR=value\n")
            f.flush()
            temp_path = f.name

        try:
            parser = EnvParser(temp_path)
            value = parser.get("MISSING_VAR", "str", "default_value")
            assert value == "default_value"
        finally:
            os.unlink(temp_path)


@pytest.mark.unit
class TestEnvParserDataTypes:
    """Test suite for EnvParser data type handling."""

    def test_env_parser_parse_float(self):
        """Test parsing float values."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("FLOAT_VAR=3.14\n")
            f.flush()
            temp_path = f.name

        try:
            parser = EnvParser(temp_path)
            value = parser.get("FLOAT_VAR", "float")
            assert value == 3.14
            assert isinstance(value, float)
        finally:
            os.unlink(temp_path)

    def test_env_parser_parse_list(self):
        """Test parsing list values."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("LIST_VAR=[1,2,3]\n")
            f.flush()
            temp_path = f.name

        try:
            parser = EnvParser(temp_path)
            value = parser.get("LIST_VAR", "list")
            # The parser should return a list or parsed structure
            assert value is not None
        finally:
            os.unlink(temp_path)

    def test_env_parser_parse_dict(self):
        """Test parsing dictionary values."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write('DICT_VAR={"key":"value"}\n')
            f.flush()
            temp_path = f.name

        try:
            parser = EnvParser(temp_path)
            value = parser.get("DICT_VAR", "dict")
            # The parser should return a dict or parsed structure
            assert value is not None
        finally:
            os.unlink(temp_path)
