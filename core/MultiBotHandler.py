import json
from core.Logger import Logger
from from_root import from_root
from core.EnvParser import EnvParser


class MultiBotHandler:
    def __init__(self):
        # Initialize environment and logger
        env: EnvParser = EnvParser(from_root(".env"))
        self.logger: Logger = Logger("MultiBotHandler").get_logger()
        self.current_bot_variant: str = env.get("BOT_VARIANT", "str", "somebotvalue")
        self.multi_bot_config: dict = {}

    def retrieve_multi_bot_config(self) -> None:
        """
        Reads and loads the multi-bot configuration from a JSON file.
        """
        try:
            with open(from_root("config/multi-bot.json"), "r") as f:
                self.multi_bot_config = json.load(f)
        except FileNotFoundError:
            self.logger.error("The file [config/multi-bot.json] was not found.")
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON from [config/multi-bot.json]. Error: {e}")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred while reading [config/multi-bot.json]. Error: {e}")
        else:
            self.logger.info("Successfully loaded the multi-bot configuration.")

    def should_ignore_commands(self, server_id: int) -> bool:
        """
        Determines if the current bot should ignore commands for the specified server.

        Args:
            server_id (int): The ID of the server to check.

        Returns:
            bool: True if the current bot should ignore commands, False otherwise.
        """
        self.retrieve_multi_bot_config()
        
        # Check if config and servers are valid
        if not self.multi_bot_config or not self.multi_bot_config.get("servers"):
            return False
        
        servers: list = self.multi_bot_config["servers"]

        # Iterate through servers in the config
        for server in servers:
            if server.get("server_id") == server_id:
                # Check for variants configuration
                bot_variants = server.get("bot-variants", {})
                primary_variant = bot_variants.get("primary")
                other_variants = bot_variants.get("others", [])

                # If current bot is the primary variant, allow commands
                if primary_variant and self.current_bot_variant == primary_variant:
                    return False
                
                # If current bot is listed in other variants, ignore commands
                if self.current_bot_variant in other_variants:
                    self.logger.info(
                        f"Server {server_id}: Current bot variant [{self.current_bot_variant}] is in 'others'. Ignoring commands."
                    )
                    return True

        # If no matching server or variants are found, allow commands
        return False
