class BaseDiscordEvent:
    EVENT_NAME = None

    def __init__(self, bot):
        self.bot = bot

    async def main(self, *args, **kwargs):
        """Override in subclasses."""
        raise NotImplementedError
