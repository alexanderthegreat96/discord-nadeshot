from discord.ext import commands
from core.Logger import Logger


class TestNothing:
    def __init__(self, bot: commands.Bot, logger: Logger):
        self.bot: commands.Bot = bot
        self.logger: Logger = logger

    async def main(self):
        self.logger.info("Task: TestNothing has started...")
