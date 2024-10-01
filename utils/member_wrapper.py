import discord
from typing import List, Union, Optional, Dict
import datetime

class MemberWrapper:
    def __init__(self, member: discord.Member):
        self.member = member

    # Attribute-specific Getters
    def get_accent_color(self) -> Optional[discord.Colour]:
        return self.member.accent_color

    def get_accent_colour(self) -> Optional[discord.Colour]:
        return self.member.accent_colour

    def get_activities(self) -> List[discord.Activity]:
        return self.member.activities

    def get_activity(self) -> Optional[discord.Activity]:
        return self.member.activity

    def get_avatar(self) -> Optional[str]:
        return str(self.member.avatar.url) if self.member.avatar else None

    def get_avatar_decoration(self) -> Optional[str]:
        return self.member.avatar_decoration

    def get_avatar_decoration_sku_id(self) -> Optional[str]:
        return self.member.avatar_decoration_sku_id

    def get_banner(self) -> Optional[str]:
        return str(self.member.banner.url) if self.member.banner else None

    def is_bot(self) -> bool:
        return self.member.bot

    def get_color(self) -> Optional[discord.Colour]:
        return self.member.color

    def get_colour(self) -> Optional[discord.Colour]:
        return self.member.colour

    def get_created_at(self) -> str:
        return self.member.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_age_in_days(self) -> int:
        today = datetime.datetime.now().date()
        user_creation_date = self.member.created_at.date()
        return (today - user_creation_date).days
    
    def get_default_avatar(self) -> str:
        return str(self.member.default_avatar.url)

    def get_desktop_status(self) -> discord.Status:
        return self.member.desktop_status

    def get_discriminator(self) -> str:
        return self.member.discriminator

    def get_display_avatar(self) -> str:
        return str(self.member.display_avatar.url)

    def get_display_banner(self) -> Optional[str]:
        return self.member.display_banner

    def get_display_icon(self) -> Optional[str]:
        return str(self.member.display_icon) if self.member.display_icon else None

    def get_display_name(self) -> str:
        return self.member.display_name

    def get_dm_channel(self) -> Optional[discord.DMChannel]:
        return self.member.dm_channel

    def get_flags(self) -> discord.UserFlags:
        return self.member.flags

    def get_global_name(self) -> str:
        return self.member.global_name

    def get_guild(self) -> discord.Guild:
        return self.member.guild

    def get_guild_avatar(self) -> Optional[str]:
        return str(self.member.guild_avatar.url) if self.member.guild_avatar else None

    def get_guild_banner(self) -> Optional[str]:
        return self.member.guild_banner

    def get_guild_permissions(self) -> discord.Permissions:
        return self.member.guild_permissions

    def get_id(self) -> int:
        return self.member.id

    def get_joined_at(self) -> str:
        return self.member.joined_at.strftime("%Y-%m-%d %H:%M:%S") if self.member.joined_at else "N/A"

    def get_mention(self) -> str:
        return self.member.mention

    def get_mobile_status(self) -> discord.Status:
        return self.member.mobile_status

    def get_mutual_guilds(self) -> List[discord.Guild]:
        return self.member.mutual_guilds

    def get_name(self) -> str:
        return self.member.name

    def get_nickname(self) -> Optional[str]:
        return self.member.nick

    def is_pending(self) -> bool:
        return self.member.pending

    def get_premium_since(self) -> Optional[str]:
        return self.member.premium_since.strftime("%Y-%m-%d %H:%M:%S") if self.member.premium_since else None

    def get_public_flags(self) -> discord.PublicUserFlags:
        return self.member.public_flags

    def get_raw_status(self) -> str:
        return self.member.raw_status

    def get_resolved_permissions(self) -> discord.Permissions:
        return self.member.resolved_permissions

    def get_roles(self) -> List[str]:
        return [role.name for role in self.member.roles]  # List of role names

    def get_status(self) -> discord.Status:
        return self.member.status

    def is_system(self) -> bool:
        return self.member.system

    def get_timed_out_until(self) -> Optional[str]:
        return self.member.timed_out_until.strftime("%Y-%m-%d %H:%M:%S") if self.member.timed_out_until else None

    def get_top_role(self) -> str:
        return self.member.top_role.name

    def get_voice(self) -> Optional[discord.VoiceState]:
        return self.member.voice

    def get_web_status(self) -> discord.Status:
        return self.member.web_status

    # Method to gather all member information in a structured dictionary
    def get_member_info(self) -> Dict[str, Union[str, int, bool, Optional[str], List[str], discord.Status, List[discord.Guild]]]:
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
            "accent_color": str(self.get_accent_color()) if self.get_accent_color() else None,
        }
