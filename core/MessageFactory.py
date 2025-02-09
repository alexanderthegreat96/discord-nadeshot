from typing import Union, Dict


class MessageFactory:
    """
    A factory class for building message dictionaries that can be sent
    to Redis (or any queue) and later consumed for direct or channel messages.
    """

    @staticmethod
    def create_direct_message(user_id: int, to_send: Union[str, Dict] = None) -> dict:
        """
        Create a dictionary representing a direct message to a specific user.

        :param user_id: The Discord user ID to receive the DM.
        :param to_send: The actual content to send (string or embed dict).
        :return: A dictionary that can be serialized and pushed to a queue.
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
        Create a dictionary for a message intended for a server channel.

        :param server_id: The Discord server (guild) ID.
        :param channel_id: The Discord channel ID in that server.
        :param to_send: The actual content to send (string or embed dict).
        :param user_id: Optionally track a user who triggered this message (0 if irrelevant).
        :return: A dictionary that can be serialized and pushed to a queue.
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
        A more generic method if you have other 'message_type' values
        or more advanced use cases.

        :param message_type: Type of the message (e.g. "regular_message", "direct_message", etc.)
        :param server_id: Optional server (guild) ID.
        :param channel_id: Optional channel ID.
        :param user_id: Optional user ID.
        :param to_send: Content to send (string or embed dict).
        :return: A dictionary representing a custom message payload.
        """
        message_content = {
            "message_type": message_type,
            "server_id": server_id,
            "channel_id": channel_id,
            "user_id": user_id,
            "to_send": to_send,
        }
        return message_content
