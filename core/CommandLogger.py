from discord.ext import commands
from utils.message_wrapper import MessageWrapper
from core.Config import Config
from core.Logger import Logger


class CommandLogger:
    def __init__(
        self, logger: Logger, context: commands.Context, command_data: dict = None
    ):
        config: Config = Config()
        self.logger: Logger = logger
        self.bot_variant: str = config.env().get("BOT_VARIANT", "str", "isac-v2-master")
        self.message_wrapper: MessageWrapper = MessageWrapper(context.message)
        self.command_data: dict = command_data

    def log(self) -> None:
        self.logger.info(
            f"Logging command: {self.message_wrapper.get_content()} with params: {self.command_data}"
        )
