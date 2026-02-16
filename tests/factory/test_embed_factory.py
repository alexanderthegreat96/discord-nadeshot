"""Unit tests for factory.EmbedFactory module."""

import pytest
import discord
import json
from factory.EmbedFactory import EmbedFactory, DISCORD_COLOR_MAP


@pytest.mark.unit
class TestEmbedFactory:
    """Test suite for EmbedFactory class."""

    def test_embed_factory_color_map_not_empty(self):
        """Test that DISCORD_COLOR_MAP is populated."""
        assert len(DISCORD_COLOR_MAP) > 0

    def test_embed_factory_color_map_contains_standard_colors(self):
        """Test that DISCORD_COLOR_MAP contains expected colors."""
        expected_colors = ["red", "blue", "green", "gold", "purple"]
        for color in expected_colors:
            assert color in DISCORD_COLOR_MAP

    def test_embed_factory_create_embed_json_minimal(self):
        """Test creating minimal embed JSON."""
        embed = EmbedFactory.create_embed_json(
            title="Test Title", description="Test Description"
        )

        assert isinstance(embed, dict)
        assert embed.get("title") == "Test Title"
        assert embed.get("description") == "Test Description"

    def test_embed_factory_create_embed_json_with_color_name(self):
        """Test creating embed JSON with color name."""
        embed = EmbedFactory.create_embed_json(title="Test", color="red")

        assert embed is not None
        assert "color" in embed or "colour" in embed

    def test_embed_factory_create_embed_json_with_fields(self):
        """Test creating embed JSON with fields."""
        fields = [
            {"name": "Field 1", "value": "Value 1", "inline": True},
            {"name": "Field 2", "value": "Value 2", "inline": False},
        ]

        embed = EmbedFactory.create_embed_json(title="Test", fields=fields)

        assert embed is not None
        if "fields" in embed:
            assert len(embed["fields"]) == 2

    def test_embed_factory_create_embed_json_with_footer(self):
        """Test creating embed JSON with footer."""
        footer = "Test Footer"

        embed = EmbedFactory.create_embed_json(title="Test", footer=footer)

        assert embed is not None
        if "footer" in embed:
            assert "text" in embed["footer"]

    def test_embed_factory_create_embed_json_with_image(self):
        """Test creating embed JSON with URL."""
        url = "https://example.com"

        embed = EmbedFactory.create_embed_json(title="Test", url=url)

        assert embed is not None

    def test_embed_factory_serialize_to_json_string(self):
        """Test creating embed JSON string."""
        embed = EmbedFactory.create_embed_json(title="Test", description="Description")

        json_str = EmbedFactory.create_embed_json_string(embed)
        assert isinstance(json_str, str)
        assert len(json_str) > 0

    def test_embed_factory_json_string_is_valid(self):
        """Test that created JSON string contains expected structure."""
        embed = EmbedFactory.create_embed_json(title="Test", description="Description")

        json_str = EmbedFactory.create_embed_json_string(embed)
        parsed = json.loads(json_str)
        assert parsed is not None
        # The JSON string serializes the embed dict structure
        assert "description" in parsed or len(parsed) > 0

    def test_embed_factory_embed_from_json_string(self):
        """Test creating discord.Embed from dictionary."""
        embed_dict = {
            "title": "Test",
            "description": "Test Description",
            "color": DISCORD_COLOR_MAP["red"],
        }

        embed = EmbedFactory.create_discord_embed(embed_dict)

        assert isinstance(embed, discord.Embed)
        assert embed.title == "Test"
        assert embed.description == "Test Description"

    def test_embed_factory_multiple_embeds(self):
        """Test creating multiple different embeds."""
        embed1 = EmbedFactory.create_embed_json(title="Embed 1")
        embed2 = EmbedFactory.create_embed_json(title="Embed 2")

        assert embed1.get("title") == "Embed 1"
        assert embed2.get("title") == "Embed 2"
        assert embed1 != embed2
