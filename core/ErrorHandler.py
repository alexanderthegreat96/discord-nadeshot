from core.Logger import Logger
from discord.ext import commands
from utils.message_wrapper import MessageWrapper


class ErrorHandler:
    """
    Handles error processing for a Discord bot, including logging, publishing error logs,
    and saving error details into a database.
    """

    def __init__(
        self, ctx: commands.Context, error: str, traceback: str, logger: Logger
    ) -> None:
        """
        Initialize the error handler with necessary context, error details, and utilities.

        :param ctx: The Discord commands context.
        :param error: A string representation of the error.
        :param traceback: The traceback of the error.
        :param logger: An instance of Logger for logging error messages.
        """
        self.context: commands.Context = ctx
        self.message: str = self.context.message.content
        self.error: str = error
        self.traceback: str = traceback
        self.logger: Logger = logger

        self.message_wrapper: MessageWrapper = MessageWrapper(self.context.message)

    async def main(self) -> None:
        """
        Main method to handle the error: logs error details, publishes logs to a queue,
        and attempts to save the error details into a database.
        """
        # Log the error message and traceback
        self.logger.error(f"Something happened: {self.message} - {self.error}")
        self.logger.error(f"Error traceback: {self.traceback}")
