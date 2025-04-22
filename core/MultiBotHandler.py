import json
from core.Logger import Logger
from from_root import from_root
from core.EnvParser import EnvParser


class MultiBotHandler:
    """
    MultiBotHandler manages logic for handling multiple bot variants across different servers.

    WARNING:
        This class is a critical part of the bot's multi-variant management system.
        **Do NOT modify this class.** Improper changes can disrupt the bot's ability to
        correctly handle commands for different bot variants.

        If you need to adapt behavior, do so via configuration in `config/multi-bot.json`,
        or consult the development team for safe extension points.
    """

    def __init__(self):
        """
        Initializes the MultiBotHandler, sets up environment parsing, logging,
        and prepares to load multi-bot configurations.
        """
        env: EnvParser = EnvParser(from_root(".env"))
        self.logger: Logger = Logger("MultiBotHandler").get_logger()
        self.current_bot_variant: str = env.get("BOT_VARIANT", "str", "somebotvalue")
        self.multi_bot_config: dict = {}

    def retrieve_multi_bot_config(self) -> None:
        """
        Reads and loads the multi-bot configuration from a JSON file.

        Loads the configuration into self.multi_bot_config.
        Handles file not found, JSON parsing errors, and unexpected exceptions
        with appropriate logging.

        File Path:
            config/multi-bot.json
        """
        try:
            with open(from_root("config/multi-bot.json"), "r") as f:
                self.multi_bot_config = json.load(f)
        except FileNotFoundError:
            self.logger.error("The file [config/multi-bot.json] was not found.")
        except json.JSONDecodeError as e:
            self.logger.error(
                f"Failed to parse JSON from [config/multi-bot.json]. Error: {e}"
            )
        except Exception as e:
            self.logger.error(
                f"An unexpected error occurred while reading [config/multi-bot.json]. Error: {e}"
            )
        else:
            self.logger.info("Successfully loaded the multi-bot configuration.")

    def should_ignore_commands(self, server_id: int) -> bool:
        """
        Determines if the current bot should ignore commands for the specified server.

        This logic is based on the bot variant assigned in the multi-bot configuration.
        Each server can define a 'primary' bot variant allowed to handle commands,
        and 'other' variants that should ignore commands.

        Args:
            server_id (int): The ID of the server to check.

        Returns:
            bool:
                - True if the current bot variant should ignore commands for this server.
                - False if the bot is allowed to handle commands.
        """
        self.retrieve_multi_bot_config()

        if not self.multi_bot_config or not self.multi_bot_config.get("servers"):
            return False  # Default to allowing commands if no config is present.

        servers: list = self.multi_bot_config["servers"]

        for server in servers:
            if server.get("server_id") == server_id:
                bot_variants = server.get("bot-variants", {})
                primary_variant = bot_variants.get("primary")
                other_variants = bot_variants.get("others", [])

                if primary_variant and self.current_bot_variant == primary_variant:
                    return False  # Current bot is primary, do not ignore commands.

                if self.current_bot_variant in other_variants:
                    self.logger.info(
                        f"Server {server_id}: Current bot variant [{self.current_bot_variant}] is in 'others'. Ignoring commands."
                    )
                    return True  # Current bot is in 'others', ignore commands.

        return False  # No specific rule found, allow commands.
