import discord
from discord.ext import commands


class DiscordServer:
    def __init__(self, ctx: commands.Context):
        if ctx.channel.type == discord.ChannelType.private:
            self._discord_name: str = "direct_message"
            self._server_id: int = 0
            self._server_name: str = "direct_message"
        else:
            self._server_name: str = ctx.guild.name
            self._server_id: int = ctx.guild.id
            self._discord_name: str = ctx.guild.name

    @property
    def server_name(self) -> str:
        """Return the server's name."""
        return self._server_name

    @property
    def server_id(self) -> int:
        """Return the server's ID."""
        return self._server_id

    @property
    def discord_name(self) -> str:
        """Return the Discord name of the server."""
        return self._discord_name

    def __str__(self) -> str:
        """Return a string representation of the Server."""
        return f"Server(Name: {self.server_name}, ID: {self.server_id}, Type: {self.discord_name})"

    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return f"Server(server_id={self.server_id}, server_name={self.server_name}, discord_name={self.discord_name})"
