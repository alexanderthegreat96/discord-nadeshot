from utils.member_wrapper import MemberWrapper
from utils.guild_wrapper import GuildWrapper
from core.Logger import Logger


class OnMemberJoin:
    def __init__(self, member, bot):
        self.member = member
        self.bot = bot

        self.logger = Logger("Event: OnMemberJoin").get_logger()
        self.member_wrapper = MemberWrapper(self.member)
        self.guild_wrapper = GuildWrapper(self.member_wrapper.get_guild())

    async def main(self):
        self.logger.success(
            f"Member: {self.member_wrapper.get_name()} has joined: {self.guild_wrapper.guild_name()}"
        )
