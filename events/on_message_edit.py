import discord
from discord.ext import commands
from core.Logger import Logger
from utils.message_wrapper import MessageWrapper


class OnMessageEdit:
    """
    OnMessageEdit is an event handler triggered when a message is edited in a Discord guild.

    You are **encouraged to customize** this class to define your own logic for handling message edits.

    Example Customizations:
        - Log the original and edited message content to a moderation log.
        - Detect and respond to edits that bypass content filters.
        - Track frequent editors for moderation.
        - Save edit histories for audit purposes.

    Attributes:
        before (discord.Message): The original message before the edit.
        after (discord.Message): The message after it was edited.
        bot (commands.Bot): The bot instance handling the event.
        logger (Logger): Logger instance for recording edit events.
        message_wrapper_before (MessageWrapper): Utility wrapper for the original message.
        message_wrapper_after (MessageWrapper): Utility wrapper for the edited message.
    """

    def __init__(
        self, before: discord.Message, after: discord.Message, bot: commands.Bot
    ):
        """
        Initialize the OnMessageEdit event handler.

        Args:
            before (discord.Message): The original message before the edit.
            after (discord.Message): The updated message after the edit.
            bot (commands.Bot): The bot instance.
        """
        self.before: discord.Message = before
        self.after: discord.Message = after
        self.bot: commands.Bot = bot

        self.logger = Logger("Event: OnMessageEdit").get_logger()
        self.message_wrapper_before: MessageWrapper = MessageWrapper(self.before)
        self.message_wrapper_after: MessageWrapper = MessageWrapper(self.after)

    async def main(self) -> None:
        """
        Main method to execute custom logic when a message is edited.

        Default behavior:
            - Logs an info message showing the before and after content.

        You can extend this method to:
            - Alert moderators about specific content changes.
            - Log edit history to a file or database.
            - Re-apply content filters or moderation checks.
        """
        self.logger.info(
            f"Message: {self.message_wrapper_before.get_content()} was changed to: {self.message_wrapper_after.get_content()}"
        )
