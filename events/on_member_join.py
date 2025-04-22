import discord
from discord.ext import commands
from utils.member_wrapper import MemberWrapper
from utils.guild_wrapper import GuildWrapper
from core.Logger import Logger


class OnMemberJoin:
    """
    OnMemberJoin is an event handler triggered when a new member joins a Discord guild (server).

    You are **encouraged to customize** this class to define your own logic for welcoming,
    logging, or managing new members.

    Example Customizations:
        - Send a welcome message to the new member or to a welcome channel.
        - Assign default roles to the new member.
        - Log the join event to a moderation log channel or database.
        - Trigger onboarding workflows or messages.

    Attributes:
        member (discord.Member): The member who joined the guild.
        bot (commands.Bot): The bot instance handling the event.
        logger (Logger): Logger instance for recording join events.
        member_wrapper (MemberWrapper): Utility wrapper for the member.
        guild_wrapper (GuildWrapper): Utility wrapper for the guild.
    """

    def __init__(self, member: discord.Member, bot: commands.Bot):
        """
        Initialize the OnMemberJoin event handler.

        Args:
            member (discord.Member): The member who joined the guild.
            bot (commands.Bot): The bot instance.
        """
        self.member: discord.Member = member
        self.bot: commands.Bot = bot

        self.logger = Logger("Event: OnMemberJoin").get_logger()
        self.member_wrapper: MemberWrapper = MemberWrapper(self.member)
        self.guild_wrapper: GuildWrapper = GuildWrapper(self.member_wrapper.get_guild())

    async def main(self) -> None:
        """
        Main method to execute custom logic when a member joins.

        Default behavior:
            - Logs a success message with the member and guild name.

        You can extend this method to:
            - Send welcome DMs or channel messages.
            - Assign roles automatically.
            - Save join info for analytics or moderation.
        """
        self.logger.success(
            f"Member: {self.member_wrapper.get_name()} has joined: {self.guild_wrapper.guild_name()}"
        )
