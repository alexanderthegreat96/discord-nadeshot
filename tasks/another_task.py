class AnotherTask:
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger

    async def main(self):
        self.logger.info("Task: AnotherTask has started...")
