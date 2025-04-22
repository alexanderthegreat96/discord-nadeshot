import discord
from discord.ext import commands
from utils.member_wrapper import MemberWrapper
from utils.guild_wrapper import GuildWrapper
from core.Logger import Logger


class OnMemberUnban:
    """
    OnMemberUnban is an event handler triggered when a member is unbanned from a Discord guild (server).

    You are **encouraged to customize** this class to define your own logic when a user is unbanned.

    Example Customizations:
        - Log detailed unban information.
        - Notify moderators or a specific log channel.
        - Record unban actions in a database.
        - Trigger follow-up actions like welcome-back messages (if they rejoin).

    Attributes:
        guild (discord.Guild): The guild from which the member was unbanned.
        member (discord.User): The user who was unbanned.
        bot (commands.Bot): The bot instance handling the event.
        member_wrapper (MemberWrapper): Utility wrapper for the user.
        guild_wrapper (GuildWrapper): Utility wrapper for the guild.
        logger (Logger): Logger instance for recording unban events.
    """

    def __init__(self, guild: discord.Guild, member: discord.User, bot: commands.Bot):
        """
        Initialize the OnMemberUnban event handler.

        Args:
            guild (discord.Guild): The guild where the unban occurred.
            member (discord.User): The user who was unbanned.
            bot (commands.Bot): The bot instance.
        """
        self.guild: discord.Guild = guild
        self.member: discord.User = member
        self.bot: commands.Bot = bot

        self.member_wrapper: MemberWrapper = MemberWrapper(self.member)
        self.guild_wrapper: GuildWrapper = GuildWrapper(self.guild)
        self.logger = Logger("Event: OnMemberUnban").get_logger()

    async def main(self) -> None:
        """
        Main method to execute custom logic when a member is unbanned.

        Default behavior:
            - Logs a warning message with the user and guild name.

        You can extend this method to:
            - Notify a mod-log channel.
            - Save unban data for audit purposes.
            - Handle follow-up workflows, if applicable.
        """
        self.logger.warning(
            f"Member {self.member_wrapper.get_name()} got unbanned from: {self.guild_wrapper.get_guild_name()}"
        )
