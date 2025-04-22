import discord
from typing import Optional


class MessageWrapper:
    """
    MessageWrapper is a utility class that simplifies access to various attributes
    of a Discord message.

    This class is useful for logging, debugging, or processing message metadata
    in a consistent and readable way.

    You are **encouraged to customize** this class if you need to:
        - Add additional message context or computed fields.
        - Format messages differently for logging or analytics.
        - Integrate message data with external systems.

    Attributes:
        _message_id (int): The unique ID of the message.
        _content (str): The content of the message.
        _channel_name (str): Name of the channel where the message was sent.
        _channel_id (int): ID of the channel.
        _author_id (int): ID of the message author.
        _author_name (str): Username of the message author.
        _global_name (str): Global display name of the author.
        _author_is_bot (bool): Whether the author is a bot.
        _guild_name (str): Name of the guild or "direct_message".
        _guild_id (Optional[int]): ID of the guild or None for DMs.
        _message_type (discord.MessageType): Type of the message.
        _message_flags (discord.MessageFlags): Flags associated with the message.
        _message_creation_time (datetime): Timestamp of when the message was created.
    """

    def __init__(self, message: discord.Message):
        """
        Initialize the MessageWrapper.

        Args:
            message (discord.Message): The message object to wrap.
        """
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
        """
        Return a dictionary with detailed message information.

        Returns:
            dict: Dictionary containing key metadata about the message.
        """
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

    # ---- Individual Getters ----

    def get_message_id(self) -> int:
        """Return the message ID."""
        return self._message_id

    def get_content(self) -> str:
        """Return the content of the message."""
        return self._content

    def get_channel_name(self) -> str:
        """Return the name of the channel."""
        return self._channel_name

    def get_channel_id(self) -> int:
        """Return the ID of the channel."""
        return self._channel_id

    def get_author_id(self) -> int:
        """Return the author's user ID."""
        return self._author_id

    def get_author_name(self) -> str:
        """Return the author's username."""
        return self._author_name

    def get_global_name(self) -> Optional[str]:
        """Return the author's global display name."""
        return self._global_name

    def is_author_bot(self) -> bool:
        """Return True if the author is a bot."""
        return self._author_is_bot

    def get_guild_name(self) -> str:
        """Return the guild name or 'direct_message'."""
        return self._guild_name

    def get_guild_id(self) -> Optional[int]:
        """Return the guild ID or None for DMs."""
        return self._guild_id

    def get_message_type(self) -> discord.MessageType:
        """Return the message type."""
        return self._message_type

    def get_message_flags(self) -> discord.MessageFlags:
        """Return the message flags."""
        return self._message_flags

    def get_message_creation_time(self) -> int:
        """
        Return the message creation time as a Unix timestamp.

        Returns:
            int: The Unix timestamp of message creation.
        """
        return int(self._message_creation_time.timestamp())

    def __str__(self):
        """Return a readable string representation of the message."""
        return f"Message(id={self._message_id}, author={self._author_name}, content='{self._content}')"
