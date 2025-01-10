from os import path
import re
import os
import json
from from_root import from_root


class GenerateCommand:
    def __init__(self, input=None, prefix="/"):
        self.input = input
        self.prefix = prefix
        # generate commands.json in case it doesn't exist

        if not path.exists(from_root("config/commands.json")):
            try:
                with open(from_root("config/commands.json"), "w") as f:
                    json.dump({"commands": {}}, f, indent=2)
            except Exception as e:
                print("Error opening config/commands.json. Error: " + str(e))

    def generate_command_name(self, command=None):
        if len(command) > 1:
            command.pop(0)
            return "".join(self.reformat_text(command))
        else:
            return "".join(self.reformat_text(command[0]))

    def write_py_files(self, class_name=None, file_path=None):
        if class_name and file_path:
            if "/" in file_path:
                filePath = os.path.basename(file_path)
                dirPath = os.path.dirname(file_path)

                if not path.exists("commands/" + dirPath + "/" + class_name + ".py"):
                    if not os.path.exists("commands/" + dirPath):
                        os.makedirs("commands/" + dirPath)
                    else:
                        pass

                    content = (
                        r"""from discord.ext import commands
from utils.synced import Synced
from utils.discord_server import DiscordServer
from utils.discord_user import DiscordUser

class """
                        + class_name
                        + """:
    def __init__(
        self,
        bot: commands.Bot,
        ctx: commands.Context,
        args: tuple = None,
        authorization: list = None,
        input_arguments: dict = None,
    ) -> None:
        self.bot: commands.Bot = bot
        self.ctx: commands.Context = ctx
        self.authorization: str = authorization
        self.args: tuple = args
        self.input_arguments: dict = input_arguments

        self.response: Synced = Synced(ctx)
        self.discord_server: DiscordServer = DiscordServer(ctx)
        self.discord_user: DiscordUser = DiscordUser(ctx)

    async def main(self) -> None:
        await self.response.send(
            f"```Hi, {self.discord_user.username}, you are running the command from {self.discord_server.server_name}```"
        )
        await self.response.send("```This is the """
                        + class_name
                        + """ command output within commands folder.```")
                    """
                    )
                    try:
                        openFile = open(
                            "commands/" + dirPath + "/" + class_name + ".py", "w"
                        )
                        openFile.write(content)
                        openFile.close()
                        return {
                            "status": True,
                            "message": "Command file ["
                            + filePath
                            + "] created in [commands/"
                            + dirPath
                            + "]",
                        }
                    except Exception as e:
                        return {
                            "status": False,
                            "error": "Unable to open and write data to: commands/"
                            + dirPath
                            + "/"
                            + class_name
                            + ".py. Error: "
                            + str(e),
                        }
                else:
                    return {
                        "status": False,
                        "error": "File: [commands/"
                        + dirPath
                        + "/"
                        + class_name
                        + ".py] already exists.",
                    }
            else:
                if path.exists("commands/" + class_name + ".py"):
                    return {
                        "status": False,
                        "error": "File: [commands/"
                        + class_name
                        + ".py] already exists.",
                    }
                else:
                    content = (
                        r"""from discord.ext import commands
from utils.synced import Synced
from utils.discord_server import DiscordServer
from utils.discord_user import DiscordUser

class """
                        + class_name
                        + """:
    def __init__(
        self,
        bot: commands.Bot,
        ctx: commands.Context,
        args: tuple = None,
        authorization: list = None,
        input_arguments: dict = None,
    ) -> None:
        self.bot: commands.Bot = bot
        self.ctx: commands.Context = ctx
        self.authorization: str = authorization
        self.args: tuple = args
        self.input_arguments: dict = input_arguments

        self.response: Synced = Synced(ctx)
        self.discord_server: DiscordServer = DiscordServer(ctx)
        self.discord_user: DiscordUser = DiscordUser(ctx)
        
    async def main(self) -> None:
        await self.response.send(
            f"```Hi, {self.discord_user.username}, you are running the command from {self.discord_server.server_name}```"
        )
        await self.response.send("```This is the """
                        + class_name
                        + """ command output within commands folder.```")
                        """
                    )

                    try:
                        openFile = open("commands/" + class_name + ".py", "w")
                        openFile.write(content)
                        openFile.close()
                        return {
                            "status": True,
                            "message": "Command file ["
                            + class_name
                            + ".py] created in [commands]",
                        }
                    except Exception as e:
                        return {
                            "status": False,
                            "error": "Unable to open and write data to: commands/"
                            + class_name
                            + ".py. Error: "
                            + str(e),
                        }
        else:
            return {"status": False, "error": "No class name and file path specified"}

    def capitalize_slugged_input(self, string: str) -> list:
        """
        Convert a string into a list of capitalized words.

        Args:
            string (str): The input string to be slugged and capitalized.

        Returns:
            list: A list of capitalized words.
        """
        # Split the string into words based on spaces and special characters
        words = string.replace("-", " ").replace("_", " ").split()

        # Capitalize the first letter of each word
        capitalized_words = [word.capitalize() for word in words]

        return capitalized_words

    def convert_string_to_camelcase(self, string):
        words = self.capitalize_slugged_input(string)
        words = ",".join(words)
        camelcase_words = [words[0].lower()] + [word.title() for word in words[1:]]
        return "".join(camelcase_words)

    def camelcase_to_uppercase(self, camelcase_string):
        words = re.findall(r"[A-Z]?[a-z]*", camelcase_string)
        capitalized_words = [
            word.capitalize() if word else word.lower() for word in words
        ]
        return "".join(capitalized_words)

    def reformat_text(self, text=[]):
        uppercase_list = []
        for word in text:
            if "-" in word:
                parts = word.split("-")
                capitalized_parts = [part.capitalize() for part in parts]
                uppercase_list.append("".join(capitalized_parts))
            else:
                uppercase_list.append(word.capitalize())
        return uppercase_list

    def make_command_array(
        self, command_name, command_string=None, command_file_path=None
    ):
        if command_name and command_string and command_file_path:
            return {
                command_name: {
                    "syntax": command_string,
                    "description": "Awaiting developer description",
                    "filePath": command_file_path,
                    "authorization": [],
                    "hasValue": False,
                    "slashCommand": False,
                    "middlewares": [],
                    "arguments": {},
                }
            }
        return None

    def generate_file_path(self, command=None, filename=None):
        if len(command) > 1:
            command.pop(-1)
            return "/".join(command) + "/" + filename + ".py"
        else:
            # return "" + command[0] + "/" + filename + ".py"
            return filename + ".py"

    def generate_class_name(self, command_data=None):
        command: str = ""
        if len(command_data) > 1:
            command_name = command_data[-1]

            if "-" in command_name:
                command_name_split = command_name.split("-")

                command_name_parts = ""
                for split in command_name_split:
                    command_name_parts += split.capitalize()
                return command_name_parts
            else:
                return command_name.capitalize()

        else:
            return "".join(command)

    def manipulate_commands_json(self):
        status = True
        results = []
        errors = []

        try:
            # Open the JSON file for reading
            with open(from_root("config/commands.json"), "r") as f:
                data = json.load(f)

            if "/" in self.input:
                # Handling commands with a root command structure
                command_parts = self.input.split("/")
                root_command = command_parts[0]

                command_class_name = self.generate_class_name(command_parts)
                command_name = self.generate_command_name(command_parts)

                command_string = "/" + root_command + " " + " ".join(command_parts)

                file_path = (
                    root_command
                    + "/"
                    + self.generate_file_path(command_parts, command_class_name)
                )

                command_array = self.make_command_array(
                    command_name, command_string, file_path
                )

                # Update existing command or create new root command
                if root_command in data["commands"]:
                    data["commands"][root_command]["commands"].update(command_array)
                else:
                    data["commands"][root_command] = {"commands": command_array}

            else:
                # Handling simple commands
                command_string = self.input
                command_to_list = self.reformat_text(self.input.split(" "))
                command = "".join(command_to_list)

                file_path = command + ".py"
                command_array = {
                    command: {
                        "syntax": self.prefix + command_string,
                        "description": "Awaiting developer description",
                        "filePath": file_path,
                        "authorization": [],
                        "hasValue": False,
                        "slashCommand": False,
                        "middlewares": [],
                        "arguments": {},
                    }
                }

                if command not in data["commands"]:
                    data["commands"].update(command_array)
                else:
                    return {
                        "status": True,
                        "message": f"Skipped: {self.input}, as it already exists",
                        "class_name": command,
                        "file_path": file_path,
                    }

            # Write the updated JSON data back to the file
            with open(from_root("config/commands.json"), "w") as f:
                json.dump(data, f, indent=2)

            return {
                "status": True,
                "message": f"JSON Structure for {self.input} was saved successfully",
                "class_name": command_class_name if "/" in self.input else command,
                "file_path": file_path,
            }

        except FileNotFoundError:
            return {
                "status": False,
                "message": "The commands.json file was not found.",
            }
        except json.JSONDecodeError:
            return {
                "status": False,
                "message": "Error decoding JSON data.",
            }
        except Exception as e:
            return {
                "status": False,
                "message": f"An error occurred: {str(e)}",
            }

    def save_command(self):
        write_json = self.manipulate_commands_json()
        if (
            write_json["status"]
            and "class_name" in write_json
            and "file_path" in write_json
        ):
            print(write_json["message"])

            class_name = write_json["class_name"]
            file_path = write_json["file_path"]

            write_file = self.write_py_files(class_name, file_path)

            if write_file["status"]:
                print(write_file["message"])
            else:
                print(write_file["error"])
        else:
            print(write_json["error"])
