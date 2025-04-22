import discord
from discord.ext import commands
from core.Logger import Logger
from utils.guild_wrapper import GuildWrapper


class OnGuildJoin:
    """
    OnGuildJoin is an event handler triggered when the bot joins a new Discord guild (server).

    This class provides a customizable starting point for handling logic when your bot is added to a new server.

    You are **encouraged to customize** this class to fit your bot's behavior and onboarding process.

    Example Customizations:
        - Send a welcome message to the server owner or a default channel.
        - Save guild information to a database.
        - Apply default settings or configurations for the new guild.
        - Notify your dev/admin team of new guild activity.

    Attributes:
        guild (discord.Guild): The guild (server) the bot has joined.
        bot (commands.Bot): The bot instance that joined the guild.
        guild_wrapper (GuildWrapper): Helper for accessing guild-related utilities.
        logger (Logger): Logger instance for recording event activity.
    """

    def __init__(self, guild: discord.Guild, bot: commands.Bot):
        """
        Initialize the OnGuildJoin event handler.

        Args:
            guild (discord.Guild): The guild object representing the server the bot joined.
            bot (commands.Bot): The bot instance (usually commands.Bot or AutoShardedBot).
        """
        self.guild: discord.Guild = guild
        self.bot: commands.Bot = bot

        self.guild_wrapper: GuildWrapper = GuildWrapper(self.guild)
        self.logger = Logger("Event: OnGuildJoin").get_logger()

    async def main(self) -> None:
        """
        Main method to execute custom logic when the bot joins a new guild.

        Default behavior:
            - Logs a success message with the guild name.

        You can extend this method to:
            - Perform onboarding tasks.
            - Send welcome or setup messages.
            - Save or log the guild's metadata.
            - Track events for analytics or monitoring.
        """
        self.logger.success(f"Bot joined: {self.guild_wrapper.get_guild_name()}")
