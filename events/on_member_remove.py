from utils.member_wrapper import MemberWrapper
from utils.guild_wrapper import GuildWrapper
from core.Logger import Logger

class OnMemberRemove:
    def __init__(self, member, bot):
        self.member = member
        self.bot = bot

        self.member_wrapper = MemberWrapper(self.member)
        self.guild_wrapper = GuildWrapper(self.member_wrapper.get_guild())
        self.logger = Logger("Event: OnMemberRemove").get_logger()

    async def main(self):
        # do stuff when the user leaves the server
        self.logger.warning(f"Member left {self.member_wrapper.get_name()} left from: {self.guild_wrapper.get_guild_name()}")
