from core.Logger import Logger
from utils.guild_wrapper import GuildWrapper
from utils.config import Config


class OnGuildJoin:
    def __init__(self, guild, bot):
        self.guild = guild
        self.bot = bot

        self.guild_wrapper = GuildWrapper(self.guild)
        self.logger = Logger("Event: OnGuildJoin").get_logger()

    async def main(self):
        self.logger.success(f"Bot joined: {self.guild_wrapper.get_guild_name()}")
