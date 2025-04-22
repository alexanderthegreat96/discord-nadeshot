from discord.ext import commands


class CooldownImmune:
    """
    CooldownImmune handles logic related to bypassing or checking cooldown immunity
    for a given context and user in Discord bot commands.

    This class is **meant to be customized** by the user. You can override or expand
    the logic in `main()` to define specific rules for when a user should be immune
    to cooldowns.

    Example use cases:
    - Make bot admins immune to cooldowns.
    - Allow premium users to bypass cooldowns.
    - Implement time-based immunity windows.
    """

    def __init__(self, ctx: commands.Context, user_id: int = 0):
        """
        Initializes the CooldownImmune instance.

        Args:
            ctx (commands.Context): The context in which the cooldown check is performed.
                                    Usually passed during command invocation.
            user_id (int, optional): The user ID to check for cooldown immunity.
                                     Defaults to 0 (can represent the message author or a specific user).
        """
        self.ctx: commands.Context = ctx
        self.user_id: int = user_id

    def main(self) -> bool:
        """
        Main method where the cooldown immunity logic should be implemented.

        Returns:
            bool: Whether the user is immune to cooldown.
                  Default implementation always returns True.

        Note:
            Customize this method to add your own cooldown immunity logic.
            Examples:
            - Check if self.user_id is in a list of privileged users.
            - Use ctx.author.roles to determine if a user should be immune.
            - Add database checks for special status.

        Example Custom Logic:
            if self.user_id in [123456789, 987654321]:  # Admin user IDs
                return True
            if "Moderator" in [role.name for role in self.ctx.author.roles]:
                return True
            return False
        """
        # write your logic here
        return True
