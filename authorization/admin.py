from discord.ext import commands


class Admin:
    """
    Admin is a customizable class used for implementing authorization logic within the bot.

    This class allows you to define whether a user has administrative permissions or roles
    needed to execute certain commands.

    You are **encouraged to modify** this class to implement your own authorization checks.

    Typical Use Cases:
        - Check if a user has a specific role or permission.
        - Query a database or model to retrieve user roles.
        - Allow or deny command execution based on custom criteria.

    Integration:
        - This class can be referenced in a command's authorization array.
        - You can define other classes similar to Admin for different permission levels or contexts.

    Attributes:
        ctx (commands.Context): The context in which the command is being executed.
        user_id (int): The ID of the user whose permissions are being checked.
    """

    def __init__(self, ctx: commands.Context, user_id: int = 0):
        """
        Initialize the Admin authorization checker.

        Args:
            ctx (commands.Context): The command context, containing user, guild, channel, etc.
            user_id (int): The ID of the user to check authorization for. Defaults to the context author if 0.
        """
        self.ctx: commands.Context = ctx
        self.user_id: int = (
            user_id or ctx.author.id
        )  # Default to command author if not provided

    def main(self) -> bool:
        """
        Main method to determine if the user has administrative access.

        Default behavior:
            - Returns False (no access granted).

        You should **customize this method** with your logic, for example:
            - Check if the user has a specific Discord role.
            - Verify against a list of admin user IDs.
            - Query a database for user permissions.

        Returns:
            bool: True if the user is authorized as an admin, False otherwise.
        """
        # Example customization:
        # if discord.utils.get(self.ctx.author.roles, name="Admin"):
        #     return True

        # Default implementation
        return False
