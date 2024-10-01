from discord.ext import commands


class DiscordUser:
    def __init__(self, ctx: commands.Context):
        self._user_id: int = ctx.author.id
        self._discriminator: str = ctx.author.discriminator
        self._username: str = ctx.author.name
        self._full_username: str = f"{self._username}#{self._discriminator}"

    @property
    def user_id(self) -> int:
        """Return the user's ID."""
        return self._user_id

    @property
    def discriminator(self) -> str:
        """Return the user's discriminator."""
        return self._discriminator

    @property
    def username(self) -> str:
        """Return the user's username."""
        return self._username

    @property
    def full_username(self) -> str:
        """Return the user's full username (username#discriminator)."""
        return self._full_username

    def __str__(self) -> str:
        """Return a string representation of the User."""
        return f"{self.full_username} (ID: {self.user_id})"

    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return f"User(user_id={self.user_id}, username={self.username}, discriminator={self.discriminator})"
