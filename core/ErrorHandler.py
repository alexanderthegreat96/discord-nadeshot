from core.Logger import Logger
from discord.ext import commands
from utils.message_wrapper import MessageWrapper


class ErrorHandler:
    """
    Handles error processing for a Discord bot, including logging, publishing error logs,
    and saving error details into a database.

    This class is meant to be user-editable. You can extend or modify the logic inside
    `main()` to suit your bot's specific error handling needs.
    """

    def __init__(
        self, ctx: commands.Context, error: str, traceback: str, logger: Logger
    ) -> None:
        """
        Initialize the ErrorHandler with necessary context, error details, and logging utilities.

        Args:
            ctx (commands.Context): The Discord commands context where the error occurred.
            error (str): A string representation of the error.
            traceback (str): The traceback information of the error.
            logger (Logger): An instance of Logger for recording error messages.
        """
        self.context: commands.Context = ctx
        self.message: str = self.context.message.content
        self.error: str = error
        self.traceback: str = traceback
        self.logger: Logger = logger

        self.message_wrapper: MessageWrapper = MessageWrapper(self.context.message)

    async def main(self) -> None:
        """
        Main method to handle the error:
        - Logs error details.
        - (Optionally) Publishes logs to a queue or external service.
        - (Optionally) Saves error details into a database.

        This method can be extended to notify developers, send error reports,
        or any other custom behavior you require.

        Example:
            - You can add retry logic.
            - Send a DM to the bot owner.
            - Post in a specific Discord channel.
        """
        # Basic error logging
        self.logger.error(f"Something happened: {self.message} - {self.error}")
        self.logger.error(f"Error traceback: {self.traceback}")

        # TODO: Extend this method to add more custom error handling logic.
