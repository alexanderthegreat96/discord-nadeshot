from discord.ext import commands
from core.SyncedResponse import SyncedResponse
from utils.discord_server import DiscordServer
from utils.discord_user import DiscordUser


class ThirdCommand:
    def __init__(
        self,
        bot: commands.Bot,
        ctx: commands.Context,
        args: tuple = None,
        authorization: list = None,
        input_arguments: dict = None,
    ) -> None:
        self.bot: commands.Bot = bot
        self.ctx: commands.Context = ctx
        self.authorization: str = authorization
        self.args: tuple = args
        self.input_arguments: dict = input_arguments

        self.response: SyncedResponse = SyncedResponse(ctx)
        self.discord_server: DiscordServer = DiscordServer(ctx)
        self.discord_user: DiscordUser = DiscordUser(ctx)

    async def main(self) -> None:
        await self.response.send(
            f"```Hi, {self.discord_user.username}, you are running the command from {self.discord_server.server_name}```"
        )
        await self.response.send(
            "```This is the ThirdCommand command output within commands folder.```"
        )
