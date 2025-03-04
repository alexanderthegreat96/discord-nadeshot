import os
import json
import re
from os import path
from from_root import from_root
from typing import List, Dict, Any, Tuple, Optional, Union


class GenerateCommand:
    """
    A utility class for generating Discord command files and updating a JSON
    configuration (commands.json) with relevant command metadata.
    """

    def __init__(self, input_command: str = None, prefix: str = "/") -> None:
        """
        Initializes the GenerateCommand object.

        :param input_command: The user input (command) string.
        :param prefix: The prefix to use for the command (default: "/").
        """
        self.input: str = input_command
        self.prefix: str = prefix

        # Ensure commands.json exists or initialize it
        commands_json_path = from_root("config/commands.json")
        if not path.exists(commands_json_path):
            try:
                with open(commands_json_path, "w", encoding="utf-8") as f:
                    json.dump({"commands": {}}, f, indent=2)
            except Exception as e:
                print(f"Error creating config/commands.json. Error: {e}")
        else:
            # Even if the file exists, ensure it has the "commands" key
            try:
                with open(commands_json_path, "r+", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        if "commands" not in data or not isinstance(
                            data["commands"], dict
                        ):
                            data["commands"] = {}
                            f.seek(0)
                            f.truncate()
                            json.dump(data, f, indent=2)
                    except json.JSONDecodeError:
                        # If JSON is invalid, rewrite a default structure
                        f.seek(0)
                        f.truncate()
                        json.dump({"commands": {}}, f, indent=2)
            except Exception as e:
                print(
                    f"Error ensuring 'commands' key in config/commands.json. Error: {e}"
                )

    def generate_command_name(self, command_parts: List[str]) -> str:
        """
        Generate a command name from a list of parts.
        For example, ['foo', 'bar'] -> 'FooBar'.

        :param command_parts: List of command parts (e.g., ['foo', 'bar']).
        :return: A string representing the formatted command name.
        """
        # If there's more than one part, remove the first item and combine the rest.
        if len(command_parts) > 1:
            command_parts.pop(0)
            return "".join(self.reformat_text(command_parts))
        return "".join(self.reformat_text([command_parts[0]]))

    def write_py_files(
        self, class_name: Optional[str], file_path: Optional[str]
    ) -> Dict[str, Union[bool, str]]:
        """
        Write a Python command file with a basic template.

        :param class_name: The class name to be used in the generated file.
        :param file_path: The relative path (under "commands/") where the file will be created.
        :return: A dictionary containing status and message or error.
        """
        if not class_name or not file_path:
            return {"status": False, "error": "No class name and file path specified."}

        # Extract final file and directory path
        final_file_name = os.path.basename(file_path)
        final_dir_path = os.path.dirname(file_path)

        # Full path under "commands"
        if final_dir_path:
            full_dir_path = os.path.join("commands", final_dir_path)
            full_file_path = os.path.join(full_dir_path, f"{class_name}.py")
        else:
            full_dir_path = "commands"
            full_file_path = os.path.join(full_dir_path, f"{class_name}.py")

        # Check if file already exists
        if path.exists(full_file_path):
            return {
                "status": False,
                "error": f"File: [{full_file_path}] already exists.",
            }

        # If necessary, create subdirectories
        if final_dir_path and not os.path.exists(full_dir_path):
            os.makedirs(full_dir_path, exist_ok=True)

        # Template content
        content = (
            "from discord.ext import commands\n"
            "from utils.SyncedResponse import SyncedResponse\n"
            "from utils.discord_server import DiscordServer\n"
            "from utils.discord_user import DiscordUser\n\n\n"
            f"class {class_name}:\n"
            "    def __init__(\n"
            "        self,\n"
            "        bot: commands.Bot,\n"
            "        ctx: commands.Context,\n"
            "        args: tuple = None,\n"
            "        authorization: list = None,\n"
            "        input_arguments: dict = None,\n"
            "    ) -> None:\n"
            "        self.bot: commands.Bot = bot\n"
            "        self.ctx: commands.Context = ctx\n"
            "        self.authorization: str = authorization\n"
            "        self.args: tuple = args\n"
            "        self.input_arguments: dict = input_arguments\n\n"
            "        self.response: SyncedResponse = SyncedResponse(ctx)\n"
            "        self.discord_server: DiscordServer = DiscordServer(ctx)\n"
            "        self.discord_user: DiscordUser = DiscordUser(ctx)\n\n"
            "    async def main(self) -> None:\n"
            "        await self.response.send(\n"
            '            f"```Hi, {self.discord_user.username}, you are running the command '
            f'from {{self.discord_server.server_name}}```"\n'
            "        )\n"
            f'        await self.response.send("```This is the {class_name} command '
            'output within commands folder.```")\n'
        )

        # Attempt to write file
        try:
            with open(full_file_path, "w", encoding="utf-8") as f:
                f.write(content)

            return {
                "status": True,
                "message": f"Command file [{final_file_name}] created in [{full_dir_path}].",
            }
        except Exception as e:
            return {
                "status": False,
                "error": f"Unable to open and write data to: {full_file_path}. Error: {e}",
            }

    def capitalize_slugged_input(self, string: str) -> List[str]:
        """
        Convert a string into a list of capitalized words.
        e.g. "some_string-name" -> ["Some", "String", "Name"].

        :param string: The input string to be slugged and capitalized.
        :return: A list of capitalized words.
        """
        # Split the string into words based on spaces and special characters
        words = string.replace("-", " ").replace("_", " ").split()
        # Capitalize the first letter of each word
        return [word.capitalize() for word in words]

    def convert_string_to_camelcase(self, string: str) -> str:
        """
        Convert a string with hyphens/underscores into camelCase.

        :param string: The string to convert.
        :return: The camelCase version of the string.
        """
        words = self.capitalize_slugged_input(string)
        # If words are empty or single-element, handle carefully
        if not words:
            return ""
        if len(words) == 1:
            return words[0].lower()

        # first word lower, subsequent words title-cased
        camelcase_words = [words[0].lower()] + [word.title() for word in words[1:]]
        return "".join(camelcase_words)

    def camelcase_to_uppercase(self, camelcase_string: str) -> str:
        """
        Convert a camelCase string into an uppercase-lumped string.
        e.g. "someString" -> "SomeString".

        :param camelcase_string: The string to convert.
        :return: The converted string with uppercase beginnings.
        """
        words = re.findall(r"[A-Z]?[a-z]*", camelcase_string)
        capitalized_words = [
            word.capitalize() if word else word.lower() for word in words
        ]
        return "".join(capitalized_words)

    def reformat_text(self, text_parts: List[str]) -> List[str]:
        """
        Reformat a list of words to have each word capitalized.
        Also merges hyphenated words into a single capitalized token.

        :param text_parts: The parts of the text (e.g., ["foo-bar", "baz"]).
        :return: A list of capitalized or merged tokens.
        """
        uppercase_list = []
        for word in text_parts:
            if "-" in word:
                sub_parts = word.split("-")
                capitalized_parts = [part.capitalize() for part in sub_parts]
                uppercase_list.append("".join(capitalized_parts))
            else:
                uppercase_list.append(word.capitalize())
        return uppercase_list

    def make_command_array(
        self, command_name: str, command_string: str, command_file_path: str
    ) -> Optional[Dict[str, Dict[str, Any]]]:
        """
        Build a nested dictionary structure for the given command.

        :param command_name: The name of the command (e.g., 'Ping').
        :param command_string: The full syntax string for the command.
        :param command_file_path: The path to the command file (under "commands/").
        :return: A dictionary representing the command data or None.
        """
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

    def generate_file_path(self, command_parts: List[str], filename: str) -> str:
        """
        Build a relative file path string using the given parts and filename.

        :param command_parts: List of command parts (e.g., ["admin", "kick"]).
        :param filename: The base name (e.g., "AdminKick").
        :return: A string representing the file path (e.g., "admin/kick/AdminKick.py").
        """
        if len(command_parts) > 1:
            # Remove the last part because it's used as the class name
            command_parts.pop(-1)
            return os.path.join("/".join(command_parts), f"{filename}.py")
        else:
            # For a single command, just return the filename
            return f"{filename}.py"

    def generate_class_name(self, command_data: List[str]) -> str:
        """
        Generate a class name from the last part of the command data.

        :param command_data: List of command parts (e.g., ["admin", "kick-user"]).
        :return: A string suitable for use as a Python class name (e.g., "KickUser").
        """
        if not command_data:
            return ""

        if len(command_data) == 1:
            # Single item: just capitalize or handle hyphens
            single = command_data[0]
            return "".join([part.capitalize() for part in single.split("-")])

        # For multiple items, focus on the last item
        command_name = command_data[-1]
        if "-" in command_name:
            return "".join([part.capitalize() for part in command_name.split("-")])
        return command_name.capitalize()

    def manipulate_commands_json(self) -> Dict[str, Union[bool, str]]:
        """
        Manipulate the commands.json file to add or update command structures
        based on self.input. Supports root/sub-command logic with "/" separators.

        - If the *root command* contains a dash or any special character outside [A-Za-z0-9],
          returns an error.
        - If "commands" key is missing, we create it.
        - If attempting to add a nested command to a root command that is already a single command,
          we return an error stating it is already defined.
        - If a single command is already defined at top level (e.g. "Greetings"),
          and we attempt to define it again, we skip or error out.
        """
        commands_json_path = from_root("config/commands.json")

        try:
            with open(commands_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Just in case, ensure "commands" key is there
            if "commands" not in data or not isinstance(data["commands"], dict):
                data["commands"] = {}

            # Decide if it's a nested command (contains "/") or single
            if "/" in self.input:
                command_parts = self.input.split("/")

                # The *root command* is the first part before the slash
                root_command = command_parts[0]

                # Validate the root command: no dash or special chars
                # Allowed characters: letters (A-Za-z) and digits (0-9) only
                if re.search(r"[^A-Za-z0-9]", root_command):
                    return {
                        "status": False,
                        "error": (
                            f"Cannot implement root command '{root_command}' "
                            "because it contains invalid characters (dash or special)."
                        ),
                    }

                # Capitalized key for JSON
                root_command_key = root_command.capitalize()

                # Check if a single command with the same name already exists
                # If it does, we cannot add subcommands to it.
                if root_command_key in data["commands"]:
                    existing_root_data = data["commands"][root_command_key]
                    # A single command would not have a "commands" dict
                    if (
                        isinstance(existing_root_data, dict)
                        and "commands" not in existing_root_data
                    ):
                        return {
                            "status": False,
                            "error": (
                                f"Cannot implement '{self.input}' "
                                f"because '{root_command}' is already defined as a single command."
                            ),
                        }

                command_class_name = self.generate_class_name(command_parts)
                command_name = self.generate_command_name(command_parts)

                # Use the prefix instead of hardcoded "/"
                command_string = (
                    f"{self.prefix}{root_command} {' '.join(command_parts)}"
                )

                file_path = os.path.join(
                    root_command,
                    self.generate_file_path(command_parts, command_class_name),
                )

                command_array = self.make_command_array(
                    command_name, command_string, file_path
                )

                if command_array is None:
                    return {
                        "status": False,
                        "message": "Failed to build command array.",
                    }

                # If the capitalized key does not exist or is a dict with "commands", we can add subcommands
                if root_command_key not in data["commands"]:
                    data["commands"][root_command_key] = {
                        "authorization": [],
                        "middlewares": [],
                        "commands": command_array,
                    }
                else:
                    data["commands"][root_command_key]["commands"].update(command_array)

            else:
                # Handling simple commands (no slash)
                command_string = self.input
                command_words = self.reformat_text(command_string.split(" "))
                command = "".join(command_words)
                file_path = f"{command}.py"

                # If a single command with the same name is already present, error out or skip
                if command in data["commands"]:
                    return {
                        "status": False,
                        "message": f"Skipped: {self.input}, as it already exists",
                        "class_name": command,
                        "file_path": file_path,
                    }

                # Build the command array for top-level insertion
                command_array = {
                    command: {
                        "syntax": f"{self.prefix}{command_string}",
                        "description": "Awaiting developer description",
                        "filePath": file_path,
                        "authorization": [],
                        "hasValue": False,
                        "slashCommand": False,
                        "middlewares": [],
                        "arguments": {},
                    }
                }

                data["commands"].update(command_array)

            # Write the updated JSON data back
            with open(commands_json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            return {
                "status": True,
                "message": f"JSON structure for '{self.input}' was saved successfully.",
                "class_name": command_class_name if "/" in self.input else command,
                "file_path": file_path,
            }

        except FileNotFoundError:
            return {
                "status": False,
                "error": "The commands.json file was not found.",
            }
        except json.JSONDecodeError:
            return {
                "status": False,
                "error": "Error decoding JSON data.",
            }
        except Exception as e:
            return {
                "status": False,
                "error": f"An error occurred: {str(e)}",
            }

    def save_command(self) -> None:
        """
        Public method to update the commands.json file and generate the .py file
        for the command. Prints success/error messages directly.
        """
        json_result = self.manipulate_commands_json()
        if not json_result.get("status"):
            # If we fail at the JSON step, check for an 'error' or fallback to 'message'
            error_or_msg = json_result.get("error") or json_result.get("message")
            print(error_or_msg)
            return

        print(json_result["message"])

        if "class_name" in json_result and "file_path" in json_result:
            class_name = json_result["class_name"]
            file_path = json_result["file_path"]
            write_result = self.write_py_files(class_name, file_path)

            if write_result["status"]:
                print(write_result["message"])
            else:
                print(write_result["error"])
        else:
            # The operation might have been skipped because the command already exists
            print("No class/file was created, possibly already exists.")
