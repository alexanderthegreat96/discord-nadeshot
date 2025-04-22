from discord.ext import commands


class DiscordUser:
    """
    DiscordUser is a utility class for accessing basic information about the user
    who invoked a command.

    This class simplifies access to the user's ID, username, discriminator,
    and full username (e.g., "Name#1234").

    You are **encouraged to customize** this class if you need more advanced
    user-related logic or attributes, such as:
        - Fetching roles, permissions, or presence status.
        - Interfacing with a user database.
        - Storing or manipulating user-specific data for the bot.

    Attributes:
        _user_id (int): The unique Discord ID of the user.
        _username (str): The user's username.
        _discriminator (str): The 4-digit discriminator.
        _full_username (str): The full username in "username#discriminator" format.
    """

    def __init__(self, ctx: commands.Context):
        """
        Initialize the DiscordUser instance based on the command context.

        Args:
            ctx (commands.Context): The context in which the command was triggered.
        """
        self._user_id: int = ctx.author.id
        self._discriminator: str = ctx.author.discriminator
        self._username: str = ctx.author.name
        self._full_username: str = f"{self._username}#{self._discriminator}"

    # ---- Properties ----

    @property
    def user_id(self) -> int:
        """Return the user's Discord ID."""
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

    # ---- Explicit Getter Methods ----

    def get_user_id(self) -> int:
        """Explicit getter for user_id."""
        return self._user_id

    def get_discriminator(self) -> str:
        """Explicit getter for discriminator."""
        return self._discriminator

    def get_username(self) -> str:
        """Explicit getter for username."""
        return self._username

    def get_full_username(self) -> str:
        """Explicit getter for full username."""
        return self._full_username

    # ---- Representations ----

    def __str__(self) -> str:
        """Return a readable summary of the user."""
        return f"{self.full_username} (ID: {self.user_id})"

    def __repr__(self) -> str:
        """Return a detailed string with user details."""
        return f"User(user_id={self.user_id}, username={self.username}, discriminator={self.discriminator})"
