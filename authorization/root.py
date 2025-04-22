from discord.ext import commands


class Root:
    """
    Root is a customizable class used for defining superuser or owner-level
    authorization logic within the bot.

    This class is intended for scenarios where **full control** or **highest privileges**
    are required to access certain commands, typically reserved for bot owners
    or system administrators.

    You are **encouraged to modify** this class to enforce your own "root-level" access control.

    Typical Use Cases:
        - Restrict sensitive commands (e.g., bot shutdown, configuration reload) to trusted users.
        - Define a static list of bot owners or system administrators.
        - Integrate with a permissions system or external data source.

    Integration:
        - This class can be referenced in a command's authorization array for high-privilege actions.
        - Works alongside Admin, Moderator, and other role-based classes.

    Attributes:
        ctx (commands.Context): The command context (includes author, guild, etc.).
        user_id (int): The ID of the user being checked for root-level access.
    """

    def __init__(self, ctx: commands.Context, user_id: int = 0):
        """
        Initialize the Root authorization checker.

        Args:
            ctx (commands.Context): The context in which the command is being executed.
            user_id (int): The user ID to check. Defaults to the context author if 0.
        """
        self.ctx: commands.Context = ctx
        self.user_id: int = user_id or ctx.author.id

    def main(self) -> bool:
        """
        Main method to determine if the user has root-level access.

        Default behavior:
            - Always returns True (grants access).

        You should **customize this method** to enforce stricter root access control, for example:
            - Check if the user is the bot owner.
            - Validate against a static list of superusers.
            - Check roles or permissions specifically designated for root-level commands.

        Returns:
            bool: True if the user has root access, False otherwise.
        """
        # Example customization:
        # ROOT_IDS = [111111111111111111, 222222222222222222]
        # return self.user_id in ROOT_IDS

        # Default implementation grants access
        return True
