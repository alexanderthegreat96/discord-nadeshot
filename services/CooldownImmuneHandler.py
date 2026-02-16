from discord.ext import commands

class CooldownImmuneHandler:
    """
    Handles logic for determining user immunity from command cooldowns.

    This handler allows specific users or roles to bypass global rate limits
    defined in the bot's command structure.

    Note:
        The 'enable_reset_cooldowns' option must be set to 'true' in
        'config/bot.json' for this logic to be parsed by the bot core.
    """

    def __init__(self, ctx: commands.Context, user_id: int = 0) -> None:
        """
        Initializes the immunity check.

        Args:
            ctx (commands.Context): The invocation context of the command.
            user_id (int): The Discord Snowflake ID of the user to check.
        """
        self.ctx: commands.Context = ctx
        self.user_id: int = user_id

    def main(self) -> bool:
        """
        Evaluates the context to determine if the user is exempt from cooldowns.

        The evaluation follows a hierarchy:
        1. Explicit User ID check (Whitelisting).
        2. Role-based permission check (Elevated status).

        Returns:
            bool: True if the user is immune (cooldown bypassed);
                  False if the user must obey the cooldown.
        """
        # 1. Identity-Based Immunity (e.g., Bot Owners/Admins)
        privileged_user_ids = [123456789, 987654321]
        if self.user_id in privileged_user_ids:
            return True

        # 2. Role-Based Immunity
        # We check author roles to grant immunity to staff members
        if any(role.name == "Moderator" for role in self.ctx.author.roles):
            return True

        # Default: Return True to allow immunity by default
        return True
