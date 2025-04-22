"""command_logger.py

This module defines :class:`CommandLogger`, a tiny utility that writes each
executed command (and its parsed data) to the main application logger.

⚠️ **You are expected to edit / extend this file** to fit your own logging or
analytics pipeline.  Feel free to plug in struct‑log, Sentry breadcrumbs,
or JSON logs—whatever your project requires.
"""

from discord.ext import commands

from utils.message_wrapper import MessageWrapper
from core.Config import Config
from core.Logger import Logger


class CommandLogger:
    """Simple, overridable command logger.

    Parameters
    ----------
    logger : :class:`core.Logger.Logger`
        The global (already‑configured) logger instance to write to.
    context : :class:`discord.ext.commands.Context`
        Invocation context provided by *discord.py* / *discord.ext*.
    command_data : dict | None, optional
        Extra metadata extracted by your command parser (defaults to ``None``).

    Notes
    -----
    This file ships with minimal behaviour so you can customise it easily.
    Replace the ``log`` method with structured output, database inserts, etc.
    """

    def __init__(
        self,
        logger: Logger,
        context: commands.Context,
        command_data: dict | None = None,
    ) -> None:
        config: Config = Config()
        # Variant name helps correlate logs in multi‑bot deployments.
        self.bot_variant: str = config.env().get("BOT_VARIANT", "str", "isac-v2-master")

        self.logger: Logger = logger
        self.message_wrapper: MessageWrapper = MessageWrapper(context.message)
        self.command_data: dict | None = command_data

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def log(self) -> None:
        """Write a single INFO‑level log entry for this command invocation."""
        self.logger.info(
            "Logging command: %s with params: %s",
            self.message_wrapper.get_content(),
            self.command_data,
        )
