import discord
import datetime

class GuildWrapper:
    def __init__(self, guild: discord.Guild) -> None:
        self.guild = guild
        self.guild_id = guild.id
        self.guild_name = guild.name
        self.member_count = guild.member_count
        self.owner = guild.owner  # discord.Member object
        self.region = guild.region  # Deprecated in newer versions
        self.created_at = guild.created_at
        self.icon_url = guild.icon.url if guild.icon else None
        self.description = guild.description
        self.premium_tier = guild.premium_tier
        self.boost_count = guild.premium_subscription_count
        self.features = guild.features
        self.verification_level = guild.verification_level

    def get_guild_id(self) -> int:
        return self.guild_id

    def get_guild_name(self) -> str:
        return self.guild_name

    def get_member_count(self) -> int:
        return self.member_count

    def get_owner(self) -> discord.Member:
        return self.owner

    def get_region(self) -> discord.VoiceRegion:
        return self.region

    def get_creation_date(self) -> str:
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_age_in_days(self) -> int:
        today = datetime.datetime.now().date()
        server_creation_date = self.created_at.date()
        return (today - server_creation_date).days
        
    def get_icon_url(self) -> str:
        return self.icon_url

    def get_description(self) -> str:
        return self.description or "No description available."

    def get_premium_tier(self) -> int:
        return self.premium_tier

    def get_boost_count(self) -> int:
        return self.boost_count

    def get_features(self) -> list:
        return self.features

    def get_verification_level(self) -> discord.VerificationLevel:
        return self.verification_level
