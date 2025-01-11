from os import path, makedirs
import json
from from_root import from_root
import re


class MiddlewareGeneratorCommand:
    def __init__(self, input: str = "", kind: str = "before"):
        self.input = input.replace("-", "_")
        self.type = kind.lower()

    def to_camel_case(self, input_string: str) -> str:
        # Split the string using dashes, underscores, or dots as delimiters
        parts = re.split(r"[-_.]", input_string)
        # Capitalize each part and join them together
        return "".join(part.capitalize() for part in parts)

    def make_middleware_template(self, class_name: str) -> str:
        """Generate a Python class template for a middleware."""
        template = f"""from utils.discord_user import DiscordUser
from utils.discord_server import DiscordServer
from discord.ext import commands

class {class_name}:
    def __init__(self, ctx: commands.Context, command_data: any = None):
        self.ctx = ctx
        self.server = DiscordServer(ctx)
        self.user = DiscordUser(ctx)
        self.user_id = self.user.user_id
        self.server_id = self.server.server_id

    def main(self) -> dict:
        # Add your middleware logic here
        if 3 > 4:  # Replace with actual condition
            return {{'status': False, 'error': 'Some random error'}}
        else:
            return {{'status': True, 'message': 'It is all fine'}}
    """
        return template

    def generate(self) -> None:
        middleware_name: str = f"{self.type}_{self.input}"
        class_name = self.to_camel_case(middleware_name)

        try:
            middleware_template = self.make_middleware_template(class_name)
            middleware_dir = from_root("middlewares")

            if not path.exists(middleware_dir):
                makedirs(middleware_dir)

            middleware_file_path = path.join(middleware_dir, f"{middleware_name}.py")

            if path.exists(middleware_file_path):
                print(f"Error: {middleware_file_path} already exists.")
                return

            with open(middleware_file_path, "w") as middleware_file:
                middleware_file.write(middleware_template)

            print(
                f"Middleware template for: '{middleware_name}' has been created at {middleware_file_path}"
            )

        except Exception as e:
            print(f"Unable to generate middleware for {middleware_name}. Error: {e}")
