from typing import Optional
from discord.ext import commands

from core.Logger import Logger
from utils.message_wrapper import MessageWrapper

class PublishErrorHandler:
    """
    Dispatches exception metadata to external storage or monitoring services.

    This class serves as a dedicated extension point for the `core/ErrorHandler`.
    By isolating error-reporting logic here, the main error handler remains
    focused on user-facing feedback while this class manages persistence
    (e.g., Database logging, Sentry, or Webhook alerts).
    """

    def __init__(
        self,
        context: commands.Context | None,
        error: str,
        traceback: str,
        logger: Logger,
        message_wrapper: MessageWrapper | None = None,
    ) -> None:
        """
        Initializes the error publisher with crash data and context.

        Args:
            context (commands.Context | None): The context in which the error
                occurred. May be None if the error was outside a command.
            error (str): A string representation or short summary of the exception.
            traceback (str): The full stack trace for debugging purposes.
            logger (Logger): Internal logger for recording the reporting
                process itself.
            message_wrapper (MessageWrapper | None): Optional utility for
                sending error reports back to Discord channels.
        """
        self.context: Optional[commands.Context] = context
        self.error: str = error
        self.traceback: str = traceback
        self.logger: Logger = logger
        self.message_wrapper: Optional[MessageWrapper] = message_wrapper

    def main(self) -> None:
        """
        Executes the error publication logic.

        Use this method to route the traceback and error details to your
        chosen destination.

        Example Implementations:
            - self.db.execute("INSERT INTO error_logs ...", (self.error, self.traceback))
            - self.external_service.send_alert(f"Critical Error: {self.error}")
            - self.logger.error(f"Remote log failed: {self.error}")
        """
        # Implementation logic goes here (e.g., Database insertion, API calls)
        pass