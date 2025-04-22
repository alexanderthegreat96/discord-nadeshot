from typing import Union, Dict


class MessageFactory:
    """
    MessageFactory is a utility class for building structured message payloads.

    These messages are typically sent to Redis (or similar message queues)
    for asynchronous processing and delivery to Discord users or channels.

    WARNING:
        **Do NOT modify this class.**
        This class is a core part of the bot's messaging infrastructure.
        Any changes could disrupt the ability to send messages properly
        through the queue system.

        If you need to create custom message structures, use the provided
        `create_custom_message` method.

    Purpose:
        - Ensures all messages follow a standard format.
        - Supports direct messages (DMs), channel messages, and custom types.
        - Allows serialization and queue-based handling.
    """

    @staticmethod
    def create_direct_message(user_id: int, to_send: Union[str, Dict] = None) -> dict:
        """
        Create a dictionary representing a direct (private) message to a user.

        Args:
            user_id (int): The Discord user ID to receive the DM.
            to_send (Union[str, Dict], optional): The content to send (string or embed dictionary).

        Returns:
            dict: A structured message dictionary for a direct message.
        """
        message_content = {
            "message_type": "direct_message",
            "server_id": 0,  # Not relevant for DMs
            "channel_id": 0,  # Not relevant for DMs
            "user_id": user_id,
            "to_send": to_send,
        }
        return message_content

    @staticmethod
    def create_regular_message(
        server_id: int,
        channel_id: int,
        to_send: Union[str, Dict] = None,
        user_id: int = 0,
    ) -> dict:
        """
        Create a dictionary representing a message for a server channel.

        Args:
            server_id (int): The Discord server (guild) ID.
            channel_id (int): The Discord channel ID within the server.
            to_send (Union[str, Dict], optional): The content to send (string or embed dictionary).
            user_id (int, optional): User ID associated with the message, if applicable.

        Returns:
            dict: A structured message dictionary for a server channel message.
        """
        message_content = {
            "message_type": "regular_message",
            "server_id": server_id,
            "channel_id": channel_id,
            "user_id": user_id,
            "to_send": to_send,
        }
        return message_content

    @staticmethod
    def create_custom_message(
        message_type: str,
        server_id: int = 0,
        channel_id: int = 0,
        user_id: int = 0,
        to_send: Union[str, Dict] = None,
    ) -> dict:
        """
        Create a custom message dictionary for advanced or non-standard message types.

        Args:
            message_type (str): Type of the message (e.g., "regular_message", "direct_message").
            server_id (int, optional): Server (guild) ID.
            channel_id (int, optional): Channel ID.
            user_id (int, optional): User ID.
            to_send (Union[str, Dict], optional): Content to send (string or embed dictionary).

        Returns:
            dict: A structured custom message dictionary.
        """
        message_content = {
            "message_type": message_type,
            "server_id": server_id,
            "channel_id": channel_id,
            "user_id": user_id,
            "to_send": to_send,
        }
        return message_content
