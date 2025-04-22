class BaseDiscordEvent:
    """
    BaseDiscordEvent provides a template for creating custom Discord event handlers.

    NOTE:
        This class is currently **not in use**, but it is designed for future extensions.
        You can subclass this to implement specific event handling logic for your Discord bot.

    Usage:
        - Subclass BaseDiscordEvent to create specific event hooks.
        - Override the `EVENT_NAME` with the Discord event name (e.g., 'on_message').
        - Implement the `main` method with the logic you want to execute for that event.

    Example:
        class OnMessageEvent(BaseDiscordEvent):
            EVENT_NAME = 'on_message'

            async def main(self, message):
                if message.author == self.bot.user:
                    return
                await message.channel.send("Hello!")

    Attributes:
        EVENT_NAME (str or None): The name of the Discord event to bind to. Should be set in subclasses.
    """

    EVENT_NAME = None

    def __init__(self, bot):
        """
        Initialize the BaseDiscordEvent.

        Args:
            bot: The instance of the bot (typically commands.Bot or commands.AutoShardedBot).
        """
        self.bot = bot

    async def main(self, *args, **kwargs):
        """
        Main method to handle the event.

        NOTE:
            This method must be overridden in subclasses to define the event-specific logic.

        Raises:
            NotImplementedError: If called directly from the base class.
        """
        raise NotImplementedError("Subclasses must implement this method.")
