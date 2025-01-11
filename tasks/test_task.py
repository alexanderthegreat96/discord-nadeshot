from discord.ext import commands
from core.Logger import Logger


class TestTask:
    def __init__(self, bot: commands.Bot, logger: Logger):
        self.bot: commands.Bot = bot
        self.logger: Logger = logger

    async def main(self):
        self.logger.info("Task: TestTask has started...")
