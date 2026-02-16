from core.Logger import Logger
from discord.ext import commands

from services.PublishErrorHandler import PublishErrorHandler
from utils.message_wrapper import MessageWrapper


class ErrorHandler:
    """
    Handles error processing for a Discord bot, including logging, publishing error logs,
    and saving error details into a database.

    Extend the `main()` method to customize behavior as needed.
    """

    def __init__(
        self,
        ctx: commands.Context | None,
        error: str,
        traceback: str,
        logger: Logger,
    ) -> None:
        """
        Initialize the ErrorHandler.

        Args:
            ctx (commands.Context | None): The context where the error occurred.
            error (str): A brief description or message of the error.
            traceback (str): Detailed traceback string.
            logger (Logger): Logger instance for recording logs.
        """
        self.context = ctx
        self.error = error
        self.traceback = traceback
        self.logger = logger

        # Extract message content safely
        self.message = getattr(ctx, "message", None)
        self.message_content = getattr(self.message, "content", None)

        # Prepare a wrapper only if message exists
        self.message_wrapper = MessageWrapper(self.message) if self.message else None

    async def main(self) -> None:
        """
        Perform error handling:
        - Log the error and traceback.
        - (Optionally) Notify users or developers.
        - (Optionally) Save to DB or forward to monitoring systems.
        """
        # Compose base message for logging
        context_info = (
            f"Command: {self.message_content}"
            if self.message_content
            else "No command message available."
        )

        self.logger.error(f"[ErrorHandler] {context_info}")
        self.logger.error(f"[ErrorHandler] Error: {self.error}")
        self.logger.error(f"[ErrorHandler] Traceback:\n{self.traceback}")

        # Call the service to publish errors (e.g., to a channel or external system)
        publish_errors: PublishErrorHandler = PublishErrorHandler(
            context=self.context,
            error=self.error,
            traceback=self.traceback,
            logger=self.logger,
            message_wrapper=self.message_wrapper,
        )
        publish_errors.main()
