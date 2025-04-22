import discord
from discord.ext import commands


class DiscordServer:
    """
    DiscordServer is a utility class that abstracts details about a Discord server (guild)
    or a direct message context, providing easy access to server-related information.

    This class helps unify handling between direct messages and guild messages,
    allowing cleaner logic when dealing with different context types.

    You are **encouraged to customize** this class if you need to handle more
    advanced server-related logic, such as:
        - Fetching server-specific settings or configurations.
        - Integrating with databases for guild metadata.
        - Handling special cases for certain servers.

    Attributes:
        _server_name (str): The name of the server or "direct_message" for DMs.
        _server_id (int): The server ID or 0 for DMs.
        _discord_name (str): Alias for the server name, including DMs.
    """

    def __init__(self, ctx: commands.Context):
        """
        Initialize the DiscordServer instance based on the command context.

        Args:
            ctx (commands.Context): The context in which the command was triggered.
        """
        if ctx.channel.type == discord.ChannelType.private:
            self._discord_name: str = "direct_message"
            self._server_id: int = 0
            self._server_name: str = "direct_message"
        else:
            self._server_name: str = ctx.guild.name
            self._server_id: int = ctx.guild.id
            self._discord_name: str = ctx.guild.name

    # ---- Properties ----

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

    # ---- Explicit Getter Methods ----

    def get_server_name(self) -> str:
        """Explicit getter for server_name."""
        return self._server_name

    def get_server_id(self) -> int:
        """Explicit getter for server_id."""
        return self._server_id

    def get_discord_name(self) -> str:
        """Explicit getter for discord_name."""
        return self._discord_name

    # ---- Representations ----

    def __str__(self) -> str:
        """Return a readable summary of the server."""
        return f"Server(Name: {self.server_name}, ID: {self.server_id}, Type: {self.discord_name})"

    def __repr__(self) -> str:
        """Return a detailed string with server details."""
        return f"Server(server_id={self.server_id}, server_name={self.server_name}, discord_name={self.discord_name})"
