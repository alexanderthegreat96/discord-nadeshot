import discord
import datetime
from typing import List, Union, Optional, Dict


class MemberWrapper:
    """
    MemberWrapper is a utility class that provides detailed access to various
    attributes and metadata of a Discord member.

    This class simplifies retrieving information about a user in a guild, such as
    roles, statuses, avatars, and more.

    You are **encouraged to customize** this class to:
        - Add more derived or computed properties (e.g., custom role checks).
        - Integrate with user-based configuration or moderation systems.
        - Extend to include guild-specific logic or caching.

    Attributes:
        member (discord.Member): The Discord member object to wrap.
    """

    def __init__(self, member: discord.Member):
        """
        Initialize the MemberWrapper.

        Args:
            member (discord.Member): The Discord member instance.
        """
        self.member = member

    # ---- Attribute-specific Getters ----

    def get_accent_color(self) -> Optional[discord.Colour]:
        """Return the user's accent color, if set."""
        return self.member.accent_color

    def get_accent_colour(self) -> Optional[discord.Colour]:
        """Alias for get_accent_color (alternative spelling)."""
        return self.member.accent_colour

    def get_activities(self) -> List[discord.Activity]:
        """Return the list of current activities (games, Spotify, etc.)."""
        return self.member.activities

    def get_activity(self) -> Optional[discord.Activity]:
        """Return the primary current activity."""
        return self.member.activity

    def get_avatar(self) -> Optional[str]:
        """Return the URL of the user's custom avatar, or None."""
        return str(self.member.avatar.url) if self.member.avatar else None

    def get_avatar_decoration(self) -> Optional[str]:
        """Return the avatar decoration (if available)."""
        return self.member.avatar_decoration

    def get_avatar_decoration_sku_id(self) -> Optional[str]:
        """Return the SKU ID for the avatar decoration (if available)."""
        return self.member.avatar_decoration_sku_id

    def get_banner(self) -> Optional[str]:
        """Return the URL of the user's banner, or None."""
        return str(self.member.banner.url) if self.member.banner else None

    def is_bot(self) -> bool:
        """Return True if the user is a bot."""
        return self.member.bot

    def get_color(self) -> Optional[discord.Colour]:
        """Return the member's display color (based on top role)."""
        return self.member.color

    def get_colour(self) -> Optional[discord.Colour]:
        """Alias for get_color (alternative spelling)."""
        return self.member.colour

    def get_created_at(self) -> str:
        """Return the account creation date as a formatted string."""
        return self.member.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_age_in_days(self) -> int:
        """Return the number of days since the account was created."""
        today = datetime.datetime.now().date()
        return (today - self.member.created_at.date()).days

    def get_default_avatar(self) -> str:
        """Return the URL of the default avatar."""
        return str(self.member.default_avatar.url)

    def get_desktop_status(self) -> discord.Status:
        """Return the user's desktop status (online/offline/idle/dnd)."""
        return self.member.desktop_status

    def get_discriminator(self) -> str:
        """Return the user's 4-digit discriminator."""
        return self.member.discriminator

    def get_display_avatar(self) -> str:
        """Return the URL of the user's display avatar (guild-specific or default)."""
        return str(self.member.display_avatar.url)

    def get_display_banner(self) -> Optional[str]:
        """Return the display banner URL (if available)."""
        return self.member.display_banner

    def get_display_icon(self) -> Optional[str]:
        """Return the display icon URL (if available)."""
        return str(self.member.display_icon) if self.member.display_icon else None

    def get_display_name(self) -> str:
        """Return the user's display name (nickname or username)."""
        return self.member.display_name

    def get_dm_channel(self) -> Optional[discord.DMChannel]:
        """Return the user's DM channel (if one exists)."""
        return self.member.dm_channel

    def get_flags(self) -> discord.UserFlags:
        """Return the user's flags (e.g., staff, partner)."""
        return self.member.flags

    def get_global_name(self) -> str:
        """Return the user's global display name."""
        return self.member.global_name

    def get_guild(self) -> discord.Guild:
        """Return the guild the user belongs to."""
        return self.member.guild

    def get_guild_avatar(self) -> Optional[str]:
        """Return the URL of the user's guild-specific avatar."""
        return str(self.member.guild_avatar.url) if self.member.guild_avatar else None

    def get_guild_banner(self) -> Optional[str]:
        """Return the guild banner (if any)."""
        return self.member.guild_banner

    def get_guild_permissions(self) -> discord.Permissions:
        """Return the user's permissions in the guild."""
        return self.member.guild_permissions

    def get_id(self) -> int:
        """Return the user's unique ID."""
        return self.member.id

    def get_joined_at(self) -> str:
        """Return the date the user joined the guild."""
        return (
            self.member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
            if self.member.joined_at
            else "N/A"
        )

    def get_mention(self) -> str:
        """Return a string that mentions the user."""
        return self.member.mention

    def get_mobile_status(self) -> discord.Status:
        """Return the user's mobile status."""
        return self.member.mobile_status

    def get_mutual_guilds(self) -> List[discord.Guild]:
        """Return a list of mutual guilds."""
        return self.member.mutual_guilds

    def get_name(self) -> str:
        """Return the user's username."""
        return self.member.name

    def get_username(self) -> str:
        """Alias for get_name()."""
        return self.get_name()

    def get_nickname(self) -> Optional[str]:
        """Return the user's nickname in the guild."""
        return self.member.nick

    def is_pending(self) -> bool:
        """Return True if the user is pending verification."""
        return self.member.pending

    def get_premium_since(self) -> Optional[str]:
        """Return the date the user started boosting the guild."""
        return (
            self.member.premium_since.strftime("%Y-%m-%d %H:%M:%S")
            if self.member.premium_since
            else None
        )

    def get_public_flags(self) -> discord.PublicUserFlags:
        """Return the user's public flags."""
        return self.member.public_flags

    def get_raw_status(self) -> str:
        """Return the user's raw status string."""
        return self.member.raw_status

    def get_resolved_permissions(self) -> discord.Permissions:
        """Return the user's resolved permissions."""
        return self.member.resolved_permissions

    def get_roles(self) -> List[str]:
        """Return a list of role names the user has."""
        return [role.name for role in self.member.roles]

    def get_status(self) -> discord.Status:
        """Return the user's overall status."""
        return self.member.status

    def is_system(self) -> bool:
        """Return True if the user is a system user."""
        return self.member.system

    def get_timed_out_until(self) -> Optional[str]:
        """Return when the user's timeout ends, if any."""
        return (
            self.member.timed_out_until.strftime("%Y-%m-%d %H:%M:%S")
            if self.member.timed_out_until
            else None
        )

    def get_top_role(self) -> str:
        """Return the user's highest role in the guild."""
        return self.member.top_role.name

    def get_voice(self) -> Optional[discord.VoiceState]:
        """Return the user's voice state."""
        return self.member.voice

    def get_web_status(self) -> discord.Status:
        """Return the user's web (browser) status."""
        return self.member.web_status

    def get_member_info(
        self,
    ) -> Dict[
        str,
        Union[
            str,
            int,
            bool,
            Optional[str],
            List[str],
            discord.Status,
            List[discord.Guild],
        ],
    ]:
        """
        Return a comprehensive dictionary of the user's attributes and statuses.

        Returns:
            dict: Structured user information.
        """
        return {
            "member_id": self.get_id(),
            "username": self.get_name(),
            "discriminator": self.get_discriminator(),
            "full_username": f"{self.get_name()}#{self.get_discriminator()}",
            "global_name": self.get_global_name(),
            "is_bot": self.is_bot(),
            "display_name": self.get_display_name(),
            "display_avatar": self.get_display_avatar(),
            "mention": self.get_mention(),
            "created_at": self.get_created_at(),
            "age_in_days": self.get_age_in_days(),
            "joined_at": self.get_joined_at(),
            "nickname": self.get_nickname(),
            "pending": self.is_pending(),
            "premium_since": self.get_premium_since(),
            "public_flags": self.get_public_flags().all(),
            "roles": self.get_roles(),
            "top_role": self.get_top_role(),
            "status": self.get_status().name,
            "activity": str(self.get_activity()) if self.get_activity() else "None",
            "boosting_since": self.get_premium_since(),
            "mobile_status": self.get_mobile_status().name,
            "desktop_status": self.get_desktop_status().name,
            "web_status": self.get_web_status().name,
            "guild_id": self.get_guild().id,
            "guild_name": self.get_guild().name,
            "avatar_url": self.get_avatar(),
            "banner_url": self.get_banner(),
            "default_avatar_url": self.get_default_avatar(),
            "guild_avatar_url": self.get_guild_avatar(),
            "accent_color": str(self.get_accent_color())
            if self.get_accent_color()
            else None,
        }
