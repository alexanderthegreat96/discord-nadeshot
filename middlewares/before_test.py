from utils.discord_user import DiscordUser
from utils.discord_server import DiscordServer
from discord.ext import commands


class BeforeTest:
    def __init__(self, ctx: commands.Context, command_data: any = None):
        self.ctx = ctx
        self.server = DiscordServer(ctx)
        self.user = DiscordUser(ctx)
        self.user_id = self.user.user_id
        self.server_id = self.server.server_id

    def main(self) -> dict:
        # Add your middleware logic here
        if 3 > 4:  # Replace with actual condition
            return {"status": False, "error": "Some random error"}
        else:
            return {"status": True, "message": "It is all fine"}
