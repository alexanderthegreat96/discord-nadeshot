import discord
import datetime


class UserWrapper:
    def __init__(self, user: discord.User):
        self.user = user

    def get_user_id(self) -> int:
        return self.user.id

    def get_username(self) -> str:
        return self.user.name

    def get_discriminator(self) -> str:
        return self.user.discriminator

    def get_full_username(self) -> str:
        return f"{self.user.name}#{self.user.discriminator}"

    def is_bot(self) -> bool:
        return self.user.bot

    def get_avatar_url(self) -> str:
        return (
            str(self.user.avatar.url)
            if self.user.avatar
            else str(self.user.default_avatar.url)
        )

    def get_mention(self) -> str:
        return self.user.mention

    def get_creation_date(self) -> str:
        return self.user.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_global_name(self) -> str:
        return (
            self.user.global_name if self.user.global_name else self.get_full_username()
        )

    def is_avatar_animated(self) -> bool:
        return self.user.is_avatar_animated()

    def get_public_flags(self) -> discord.PublicUserFlags:
        return self.user.public_flags

    def get_age_in_days(self) -> int:
        today = datetime.datetime.now().date()
        user_creation_date = self.user.created_at.date()
        return (today - user_creation_date).days

    def get_user_info(self) -> dict:
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
