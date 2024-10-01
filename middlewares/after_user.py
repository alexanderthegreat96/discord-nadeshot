from utils.config import Config
from utils.discord_user import DiscordUser
from utils.discord_server import DiscordServer


class AfterUser:
    def __init__(self, ctx, command_data=None):
        self.ctx = ctx
        self.server = DiscordServer(ctx)
        self.user = DiscordUser(ctx)
        self.user_id = self.user.user_id
        self.server_id = self.server.server_id

    def main(self):
        return {
            "status": True,
            "message": "Just returning a message in this after middleware",
        }
