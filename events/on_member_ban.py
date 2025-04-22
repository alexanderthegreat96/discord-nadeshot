import discord
from discord.ext import commands
from utils.member_wrapper import MemberWrapper
from utils.guild_wrapper import GuildWrapper
from core.Logger import Logger


class OnMemberBan:
    """
    OnMemberBan is an event handler triggered when a member is banned from a Discord guild (server).

    This class is **meant to be customized** to handle actions you want to take when someone is banned.

    Example Customizations:
        - Log detailed ban information to an external service.
        - Notify admins or a specific channel about the ban.
        - Save ban details to a database.
        - Trigger automated moderation actions.

    Attributes:
        guild (discord.Guild): The guild from which the member was banned.
        member (discord.Member or discord.User): The banned member.
        reason (str): The reason for the ban, if provided.
        bot (commands.Bot): The bot instance handling the event.
        member_wrapper (MemberWrapper): Utility wrapper around the member object.
        guild_wrapper (GuildWrapper): Utility wrapper around the guild object.
        logger (Logger): Logger instance for recording ban events.
    """

    def __init__(
        self,
        guild: discord.Guild,
        member: discord.User,
        reason: str,
        bot: commands.Bot,
    ):
        """
        Initialize the OnMemberBan event handler.

        Args:
            guild (discord.Guild): The guild where the ban occurred.
            member (discord.User): The user who was banned.
            reason (str): The reason for the ban, if any.
            bot (commands.Bot): The bot instance.
        """
        self.guild: discord.Guild = guild
        self.member: discord.User = member
        self.reason: str = reason
        self.bot: commands.Bot = bot

        self.member_wrapper: MemberWrapper = MemberWrapper(self.member)
        self.guild_wrapper: GuildWrapper = GuildWrapper(self.guild)
        self.logger = Logger("Event: OnMemberBan").get_logger()

    async def main(self) -> None:
        """
        Main method to execute custom logic when a member is banned.

        Default behavior:
            - Logs a warning message with member and guild information.

        You can extend this method to:
            - Send alerts to moderation channels.
            - Record ban details in a database.
            - Notify staff or server owner.
        """
        # Customize this logic as needed for your moderation workflow
        self.logger.warning(
            f"Member {self.member_wrapper.get_name()} got banned from: "
            f"{self.guild_wrapper.get_guild_name()}. Reason: {self.reason}"
        )
