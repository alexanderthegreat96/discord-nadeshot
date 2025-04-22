import discord
import datetime


class UserWrapper:
    """
    UserWrapper is a utility class designed to simplify access to
    common attributes and metadata of a Discord User.

    This class can be used for user data handling in commands,
    logging, moderation tools, or analytics.

    You are **encouraged to customize** this class if you need to:
        - Extend user profile information handling.
        - Interface with external data or user configurations.
        - Perform additional computed properties on user data.

    Attributes:
        user (discord.User): The Discord user object.
    """

    def __init__(self, user: discord.User):
        """
        Initialize the UserWrapper.

        Args:
            user (discord.User): The Discord user object.
        """
        self.user = user

    def get_user_id(self) -> int:
        """Return the user's unique Discord ID."""
        return self.user.id

    def get_username(self) -> str:
        """Return the user's username."""
        return self.user.name

    def get_discriminator(self) -> str:
        """Return the user's 4-digit discriminator."""
        return self.user.discriminator

    def get_full_username(self) -> str:
        """Return the full username in 'username#discriminator' format."""
        return f"{self.user.name}#{self.user.discriminator}"

    def is_bot(self) -> bool:
        """Return True if the user is a bot."""
        return self.user.bot

    def get_avatar_url(self) -> str:
        """
        Return the URL of the user's avatar.
        Falls back to the default avatar if no custom avatar is set.
        """
        return (
            str(self.user.avatar.url)
            if self.user.avatar
            else str(self.user.default_avatar.url)
        )

    def get_mention(self) -> str:
        """Return the mention string for the user."""
        return self.user.mention

    def get_creation_date(self) -> str:
        """Return the date the user created their account, as a formatted string."""
        return self.user.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_global_name(self) -> str:
        """
        Return the user's global display name.
        Falls back to the full username if no global name is set.
        """
        return (
            self.user.global_name if self.user.global_name else self.get_full_username()
        )

    def is_avatar_animated(self) -> bool:
        """Return True if the user's avatar is animated."""
        return self.user.is_avatar_animated()

    def get_public_flags(self) -> discord.PublicUserFlags:
        """Return the user's public flags."""
        return self.user.public_flags

    def get_age_in_days(self) -> int:
        """Return the number of days since the user's account was created."""
        today = datetime.datetime.now().date()
        user_creation_date = self.user.created_at.date()
        return (today - user_creation_date).days

    def get_user_info(self) -> dict:
        """
        Return a comprehensive dictionary of user information.

        Returns:
            dict: Structured user metadata.
        """
        return {
            "user_id": self.get_user_id(),
            "username": self.get_username(),
            "discriminator": self.get_discriminator(),
            "full_username": self.get_full_username(),
            "is_bot": self.is_bot(),
            "avatar_url": self.get_avatar_url(),
            "mention": self.get_mention(),
            "creation_date": self.get_creation_date(),
            "age_in_days": self.get_age_in_days(),
            "global_name": self.get_global_name(),
            "is_avatar_animated": self.is_avatar_animated(),
            "public_flags": self.get_public_flags().all(),  # Converts flags to a dict of boolean values
        }
