import json
import discord
from typing import Union, List, Dict

# A mapping from color names (lowercase) to their discord.Color integer values.
DISCORD_COLOR_MAP = {
    "default": discord.Color.default().value,
    "teal": discord.Color.teal().value,
    "dark_teal": discord.Color.dark_teal().value,
    "green": discord.Color.green().value,
    "dark_green": discord.Color.dark_green().value,
    "blue": discord.Color.blue().value,
    "dark_blue": discord.Color.dark_blue().value,
    "purple": discord.Color.purple().value,
    "dark_purple": discord.Color.dark_purple().value,
    "magenta": discord.Color.magenta().value,
    "dark_magenta": discord.Color.dark_magenta().value,
    "gold": discord.Color.gold().value,
    "dark_gold": discord.Color.dark_gold().value,
    "orange": discord.Color.orange().value,
    "dark_orange": discord.Color.dark_orange().value,
    "red": discord.Color.red().value,
    "dark_red": discord.Color.dark_red().value,
    "lighter_grey": discord.Color.lighter_grey().value,
    "light_grey": discord.Color.light_grey().value,
    "dark_grey": discord.Color.dark_grey().value,
    "darker_grey": discord.Color.darker_grey().value,
    "blurple": discord.Color.blurple().value,
    "greyple": discord.Color.greyple().value,
    "fuchsia": discord.Color.fuchsia().value,
    "yellow": discord.Color.yellow().value,
}


class EmbedFactory:
    @staticmethod
    def create_embed_json(
        title: str = None,
        description: str = None,
        url: str = None,
        color: Union[int, str] = None,  # can be an int or a named color
        fields: List[Dict] = None,
        footer: Union[str, Dict, None] = None,
    ) -> dict:
        """
        Generate a dictionary (JSON-like) that contains all
        the necessary data to build a Discord embed later.
        """
        if isinstance(footer, str):
            footer = {"text": footer}

        color_value = EmbedFactory._resolve_color(color)

        embed_data = {
            "title": title,
            "description": description,
            "url": url,
            "color": color_value,
            "fields": fields or [],
            "footer": footer,
        }
        return embed_data

    @staticmethod
    def create_embed_json_string(
        title: str = None,
        description: str = None,
        url: str = None,
        color: Union[int, str] = None,
        fields: List[Dict] = None,
        footer: Union[str, Dict, None] = None,
        indent: int = None,
    ) -> str:
        """
        Same as create_embed_json, but returns a JSON string instead
        of a dictionary. You can optionally specify an 'indent' value
        for pretty-printing.
        """
        embed_dict = EmbedFactory.create_embed_json(
            title=title,
            description=description,
            url=url,
            color=color,
            fields=fields,
            footer=footer,
        )
        return json.dumps(embed_dict, indent=indent)

    @staticmethod
    def create_discord_embed(embed_data: dict) -> discord.Embed:
        """
        Convert an embed_data dictionary back into a
        discord.Embed instance.
        """
        embed = discord.Embed(
            title=embed_data.get("title"),
            description=embed_data.get("description"),
            url=embed_data.get("url"),
            color=embed_data.get("color", 0),
        )

        for field in embed_data.get("fields", []):
            embed.add_field(
                name=field.get("name", "Unnamed Field"),
                value=field.get("value", "No Value"),
                inline=field.get("inline", False),
            )

        footer_data = embed_data.get("footer")
        if footer_data and "text" in footer_data:
            icon_url = footer_data.get("icon_url", None)
            embed.set_footer(
                text=footer_data.get("text"),
                icon_url=icon_url,
            )

        return embed

    @staticmethod
    def _resolve_color(color: Union[int, str, None]) -> int:
        """
        Convert a color argument into an integer (0 if invalid or None).
        """
        if color is None:
            return 0
        if isinstance(color, int):
            return color
        color_key = color.lower()
        return DISCORD_COLOR_MAP.get(color_key, 0)
