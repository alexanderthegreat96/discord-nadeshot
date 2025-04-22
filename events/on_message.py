import discord
from discord.ext import commands
from core.Logger import Logger
from utils.message_wrapper import MessageWrapper


class OnMessage:
    """
    OnMessage is an event handler triggered whenever a new message is received in a Discord guild.

    You are **encouraged to customize** this class to define your own logic for handling messages.

    Example Customizations:
        - Log message content or metadata.
        - Trigger moderation checks (e.g., bad words, spam detection).
        - Implement custom bot responses or message handlers.
        - Save message details for analytics or monitoring.

    Attributes:
        message (discord.Message): The message received.
        bot (commands.Bot): The bot instance handling the message.
        logger (Logger): Logger instance for recording message events.
        message_wrapper (MessageWrapper): Utility wrapper for the message.
        message_data (dict): Dictionary containing structured message info.
    """

    def __init__(self, message: discord.Message, bot: commands.Bot):
        """
        Initialize the OnMessage event handler.

        Args:
            message (discord.Message): The message object received.
            bot (commands.Bot): The bot instance.
        """
        self.message: discord.Message = message
        self.bot: commands.Bot = bot
        self.logger = Logger("Event: OnMessage").get_logger()

        self.message_wrapper: MessageWrapper = MessageWrapper(self.message)
        self.message_data: dict = self.message_wrapper.get_message_info()

    async def main(self) -> None:
        """
        Main method to execute custom logic when a message is received.

        Default behavior:
            - Logs a success message with the author's name and message content.

        You can extend this method to:
            - Perform moderation checks (e.g., spam detection, filters).
            - Trigger automated bot responses.
            - Forward messages to specific channels or services.
        """
        self.logger.success(
            f"User: {self.message_wrapper.get_author_name()} just sent a message with the content: {self.message_data}"
        )
