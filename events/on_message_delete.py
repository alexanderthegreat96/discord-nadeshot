import discord
from discord.ext import commands
from core.Logger import Logger
from utils.message_wrapper import MessageWrapper


class OnMessageDelete:
    """
    OnMessageDelete is an event handler triggered when a message is deleted in a Discord guild.

    You are **encouraged to customize** this class to define your own logic for handling deleted messages.

    Example Customizations:
        - Log deleted message content to a moderation log channel.
        - Track frequent message deletions by specific users.
        - Save deleted messages for audit purposes.
        - Notify admins or moderators of deleted content.

    Attributes:
        message (discord.Message): The message that was deleted.
        bot (commands.Bot): The bot instance handling the event.
        logger (Logger): Logger instance for recording deletion events.
        message_wrapper (MessageWrapper): Utility wrapper for the message.
    """

    def __init__(self, message: discord.Message, bot: commands.Bot):
        """
        Initialize the OnMessageDelete event handler.

        Args:
            message (discord.Message): The message object that was deleted.
            bot (commands.Bot): The bot instance.
        """
        self.message: discord.Message = message
        self.bot: commands.Bot = bot
        self.logger = Logger("Event: OnMessageDelete").get_logger()

        self.message_wrapper: MessageWrapper = MessageWrapper(self.message)

    async def main(self) -> None:
        """
        Main method to execute custom logic when a message is deleted.

        Default behavior:
            - Logs a warning with the author's name and the deleted message content.

        You can extend this method to:
            - Send a message to a moderation log channel.
            - Save deleted message details for review.
            - Trigger alerts for suspicious activity.
        """
        self.logger.warning(
            f"User: {self.message_wrapper.get_author_name()} deleted message: {self.message_wrapper.get_message_info()}."
        )
