from discord.ext import commands
from services.CooldownImmuneHandler import CooldownImmuneHandler

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
        cooldown_immune: CooldownImmuneHandler = CooldownImmuneHandler(self.ctx, self.user_id)
        return cooldown_immune.main()
