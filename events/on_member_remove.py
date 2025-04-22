import discord
from discord.ext import commands
from utils.member_wrapper import MemberWrapper
from utils.guild_wrapper import GuildWrapper
from core.Logger import Logger


class OnMemberRemove:
    """
    OnMemberRemove is an event handler triggered when a member leaves or is removed from a Discord guild (server).

    You are **encouraged to customize** this class to define your own logic for handling member departures.

    Example Customizations:
        - Log detailed information about the member leaving.
        - Notify moderators or a specific channel.
        - Update member counts or statistics.
        - Trigger farewell messages or analytics.

    Attributes:
        member (discord.Member): The member who left the guild.
        bot (commands.Bot): The bot instance handling the event.
        member_wrapper (MemberWrapper): Utility wrapper for the member.
        guild_wrapper (GuildWrapper): Utility wrapper for the guild.
        logger (Logger): Logger instance for recording leave events.
    """

    def __init__(self, member: discord.Member, bot: commands.Bot):
        """
        Initialize the OnMemberRemove event handler.

        Args:
            member (discord.Member): The member who left the guild.
            bot (commands.Bot): The bot instance.
        """
        self.member: discord.Member = member
        self.bot: commands.Bot = bot

        self.member_wrapper: MemberWrapper = MemberWrapper(self.member)
        self.guild_wrapper: GuildWrapper = GuildWrapper(self.member_wrapper.get_guild())
        self.logger = Logger("Event: OnMemberRemove").get_logger()

    async def main(self) -> None:
        """
        Main method to execute custom logic when a member leaves.

        Default behavior:
            - Logs a warning message with the member and guild name.

        You can extend this method to:
            - Send a farewell message.
            - Notify moderation channels.
            - Track and store leave statistics.
        """
        self.logger.warning(
            f"Member left: {self.member_wrapper.get_name()} from: {self.guild_wrapper.get_guild_name()}"
        )
