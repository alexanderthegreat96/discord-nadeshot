from utils.member_wrapper import MemberWrapper
from utils.guild_wrapper import GuildWrapper
from core.Logger import Logger

class OnMemberBan:
    def __init__(self, guild, member, bot):
        self.member = member
        self.guild = guild
        self.bot = bot

        self.member_wrapper = MemberWrapper(self.member)
        self.guild_wrapper = GuildWrapper(self.guild)
        self.logger = Logger("Event: OnMemberBan").get_logger()

    async def main(self):
        # do stuff when the user leaves the server
        self.logger.warning(f"Member {self.member_wrapper.get_name()} got banned from: {self.guild_wrapper.get_guild_name()}")
