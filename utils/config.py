import json
from from_root import from_root


class Config:
    """
    Config is a utility class for loading JSON-based configuration files used by the bot.

    This class provides static methods to read and return data from:
        - config/config.json
        - config/bot.json
        - config/staff.json
        - config/commands.json

    WARNING:
        While this class is functional, it can be **improved for better error handling and performance**.
        You are welcome to **refactor or extend** it, but ensure any changes are well-tested.

    Suggested Improvements:
        - Use context managers (`with open(...)`) to handle file closing safely.
        - Provide more specific error handling or logging.
        - Avoid returning `False` as a default error value—consider `None` or raise exceptions.
    """

    @staticmethod
    def config() -> dict or bool:
        """
        Load the main configuration from 'config/config.json'.

        Returns:
            dict: Configuration data if successful.
            bool: False if an error occurred.
        """
        try:
            with open(from_root("config/config.json"), "r") as f:
                return json.load(f)
        except Exception:
            return False

    @staticmethod
    def bot_config() -> dict or bool:
        """
        Load the bot-specific configuration from 'config/bot.json'.

        Returns:
            dict: Bot configuration (under the "config" key) if successful.
            bool: False if an error occurred.
        """
        try:
            with open(from_root("config/bot.json"), "r") as f:
                data = json.load(f)
                return data.get("config", False)
        except Exception:
            return False

    @staticmethod
    def staff_list() -> list or bool:
        """
        Load the list of staff users from 'config/staff.json'.

        Returns:
            list: List of staff users if successful.
            bool: False if an error occurred.
        """
        try:
            with open(from_root("config/staff.json"), "r") as f:
                data = json.load(f)
                return data.get("users", False)
        except Exception:
            return False

    @staticmethod
    def staff_groups() -> dict or bool:
        """
        Load staff groups from 'config/staff.json'.

        Returns:
            dict: Staff groups mapping if successful.
            bool: False if an error occurred.
        """
        try:
            with open(from_root("config/staff.json"), "r") as f:
                data = json.load(f)
                return data.get("groups", False)
        except Exception:
            return False

    @staticmethod
    def command_list() -> list or bool:
        """
        Load the command list from 'config/commands.json'.

        Returns:
            list: List of commands if successful.
            bool: False if an error occurred.
        """
        try:
            with open(from_root("config/commands.json"), "r") as f:
                data = json.load(f)
                return data.get("commands", False)
        except Exception:
            return False
