import discord
import datetime


class GuildWrapper:
    """
    GuildWrapper is a utility class that provides easy access to common
    properties and metadata of a Discord guild (server).

    This class is designed to simplify guild-related operations and improve
    readability when working with guild data in commands or events.

    You are **encouraged to customize** this class to include additional
    guild-specific logic, such as:
        - Fetching or caching custom guild settings.
        - Formatting outputs for dashboards or logs.
        - Adding computed properties like activity stats.

    Attributes:
        guild (discord.Guild): The Discord guild object.
        guild_id (int): The unique ID of the guild.
        guild_name (str): The name of the guild.
        member_count (int): Number of members in the guild.
        owner (discord.Member): The owner of the guild.
        created_at (datetime.datetime): The date and time the guild was created.
        icon_url (str): URL of the guild's icon, if available.
        description (str): The guild's description, if set.
        premium_tier (int): The boost tier level of the guild.
        boost_count (int): Number of boosts the guild has.
        features (list): Special features enabled in the guild.
        verification_level (discord.VerificationLevel): Guild's verification level.
    """

    def __init__(self, guild: discord.Guild) -> None:
        """
        Initialize the GuildWrapper with a discord.Guild object.

        Args:
            guild (discord.Guild): The guild to wrap and extract information from.
        """
        self.guild = guild
        self.guild_id = guild.id
        self.guild_name = guild.name
        self.member_count = guild.member_count
        self.owner = guild.owner
        self.created_at = guild.created_at
        self.icon_url = guild.icon.url if guild.icon else None
        self.description = guild.description
        self.premium_tier = guild.premium_tier
        self.boost_count = guild.premium_subscription_count
        self.features = guild.features
        self.verification_level = guild.verification_level

    def get_guild_id(self) -> int:
        """Return the guild's unique ID."""
        return self.guild_id

    def get_guild_name(self) -> str:
        """Return the guild's name."""
        return self.guild_name

    def get_member_count(self) -> int:
        """Return the number of members in the guild."""
        return self.member_count

    def get_owner(self) -> discord.Member:
        """Return the owner of the guild."""
        return self.owner

    def get_region(self):
        """
        Return the voice region of the guild (deprecated by Discord, may be None or irrelevant).
        """
        return getattr(
            self.guild, "region", None
        )  # Safe fallback for deprecated regions

    def get_creation_date(self) -> str:
        """Return the creation date of the guild as a formatted string."""
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_age_in_days(self) -> int:
        """Return the age of the guild in days."""
        today = datetime.datetime.now().date()
        server_creation_date = self.created_at.date()
        return (today - server_creation_date).days

    def get_icon_url(self) -> str:
        """Return the URL of the guild's icon, or None if not set."""
        return self.icon_url

    def get_description(self) -> str:
        """Return the guild's description, or a fallback message if not set."""
        return self.description or "No description available."

    def get_premium_tier(self) -> int:
        """Return the guild's premium (boost) tier."""
        return self.premium_tier

    def get_boost_count(self) -> int:
        """Return the number of boosts the guild has."""
        return self.boost_count

    def get_features(self) -> list:
        """Return a list of enabled features for the guild."""
        return self.features

    def get_verification_level(self) -> discord.VerificationLevel:
        """Return the verification level of the guild."""
        return self.verification_level
