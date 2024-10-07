import discord
from typing import Optional


class MessageWrapper:
    def __init__(self, message: discord.Message):
        self._message_id = message.id
        self._content = message.content
        self._channel_name = (
            message.channel.name
            if isinstance(message.channel, discord.TextChannel)
            else "Private Channel"
        )
        self._channel_id = message.channel.id
        self._author_id = message.author.id
        self._author_name = message.author.name
        self._global_name = message.author.global_name
        self._author_is_bot = message.author.bot
        self._guild_name = message.guild.name if message.guild else "direct_message"
        self._guild_id = message.guild.id if message.guild else None
        self._message_type = message.type
        self._message_flags = message.flags
        self._message_creation_time = message.created_at

    def get_message_info(self) -> dict:
        """Return a dictionary with message information."""
        return {
            "message_id": self._message_id,
            "content": self._content,
            "channel_name": self._channel_name,
            "channel_id": self._channel_id,
            "author_id": self._author_id,
            "author_name": self._author_name,
            "global_name": self._global_name,
            "author_is_bot": self._author_is_bot,
            "guild_name": self._guild_name,
            "guild_id": self._guild_id,
            "message_type": str(self._message_type),
            "message_flags": str(self._message_flags),
            "message_creation_time": self._message_creation_time,
        }

    # Getters for individual fields
    def get_message_id(self) -> int:
        return self._message_id

    def get_content(self) -> str:
        return self._content

    def get_channel_name(self) -> str:
        return self._channel_name

    def get_channel_id(self) -> int:
        return self._channel_id

    def get_author_id(self) -> int:
        return self._author_id

    def get_author_name(self) -> str:
        return self._author_name

    def get_global_name(self) -> Optional[str]:
        return self._global_name

    def is_author_bot(self) -> bool:
        return self._author_is_bot

    def get_guild_name(self) -> str:
        return self._guild_name

    def get_guild_id(self) -> Optional[int]:
        return self._guild_id

    def get_message_type(self) -> discord.MessageType:
        return self._message_type

    def get_message_flags(self) -> discord.MessageFlags:
        return self._message_flags

    def get_message_creation_time(self) -> discord.utils.time_snowflake:
        return int(self._message_creation_time)

    def __str__(self):
        return f"Message(id={self._message_id}, author={self._author_name}, content='{self._content}')"
