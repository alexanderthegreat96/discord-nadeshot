from utils.config import Config
from utils.discord_user import DiscordUser
from utils.discord_server import DiscordServer
import datetime


class BeforeUserAge:
    def __init__(self, ctx, command_data=None):
        self.ctx = ctx
        self.server = DiscordServer(ctx)
        self.user = DiscordUser(ctx)
        self.user_id = self.user.user_id
        self.server_id = self.server.server_id

    def main(self):
        config = Config.bot_config
        if config:
            if (
                "enable-user-age" in config
                and config["enable-user-age"]
                and "user-age-limit" in config
                and config["user-age-limit"]
            ):
                today = datetime.datetime.now().date()
                user_creation_date = self.ctx.author.created_at.date()
                days_old = (today - user_creation_date).days

                if days_old >= config["user-age-limit"]:
                    return {"status": True}
                else:
                    return {
                        "status": False,
                        "error": "Unable to run command. Account seems fresh!",
                    }
