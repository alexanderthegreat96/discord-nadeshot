from utils.guild_wrapper import GuildWrapper
from utils.user_wrapper import UserWrapper
from discord.ext.commands import Context


class BeforeCommand:
    def __init__(self, ctx: Context, command_data: dict = None) -> None:
        self.server = GuildWrapper(ctx.guild)
        self.user = UserWrapper(ctx.author)
        self.context: Context = ctx

        self.command_data: dict = command_data

    def main(self):
        full_username = self.user.get_full_username()
        server_name = self.server.get_guild_name()
        command_name = self.command_data.get("name", "global")
        command_description = self.command_data.get("description", "Some command")

        message = f"```Hello, {full_username}, executing [{command_name}] command in [{server_name}], please hold on...```"
        message += f"```{command_description}```"

        return {"status": True, "message": message}
