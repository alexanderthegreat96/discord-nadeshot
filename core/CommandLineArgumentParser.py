import json
import re
from from_root import from_root


# This file has been improved
# and refactored by GPT 4o
class CommandLineArgumentParser:
    """
    A class to parse command-line arguments from Discord-style input strings
    using configuration from commands.json.
    """

    def __init__(self, command_input: str = ""):
        self.input = self._process_input_string(command_input)
        self.commands_list = self._load_commands()
        self.command_prefixes = ["!", ".", "?", "/", ">"]

    def flatten_dict_to_list(self, input_dict: dict) -> list:
        """
        Flattens a dictionary into a list of tokens by iterating over its items.
        Each key and its corresponding value (if not None) are added sequentially
        to the list. If a value is None, only the key is added.
        """
        tokens = []
        for key, value in input_dict.items():
            tokens.append(key)
            if value is not None:
                tokens.append(value)
        return tokens

    def pair_tokens(self, tokens: any) -> dict:
        """
        Processes a list of tokens or a dictionary of tokens into overlapping key-value pairs.
        If a dictionary is provided, it will be flattened into a list first.
        Each token will be paired with the next token as its value. The last token
        will have a value of None.

        Example:
        Input: ['/dth', 'search', 'whatever']
        Output: {'/dth': 'search', 'search': 'whatever', 'whatever': None}
        """
        # If input is a dict, flatten it first
        if isinstance(tokens, dict):
            tokens = self.flatten_dict_to_list(tokens)

        result: dict = {}
        if len(tokens) > 0:
            # will ensure that the command prefixes
            # are actually skipped
            cleaned_tokens = []
            # Remove prefixes only for the first token
            for index, token in enumerate(tokens):
                if index == 0:
                    for prefix in self.command_prefixes:
                        if prefix in str(token):
                            token = token.replace(prefix, "")
                cleaned_tokens.append(token)
            tokens = cleaned_tokens

            for i in range(len(tokens)):
                key = tokens[i]
                # If there's a next token, pair with it; otherwise, pair with None
                next_value = tokens[i + 1] if (i + 1) < len(tokens) else None
                result[key] = next_value
        return result

    def _process_input_string(self, input_string: str) -> str:
        """
        Processes square-bracketed strings by replacing spaces with underscores
        within the brackets.
        Example: "command [some arg]" -> "command [some_arg]"
        """
        input_string = input_string.lower()
        pattern = r"\[(.*?)\]"
        matches = re.findall(pattern, input_string)
        if matches:
            for match in matches:
                processed_match = match.replace(" ", "_")
                input_string = input_string.replace(f"[{match}]", processed_match)
        return input_string

    def _load_commands(self):
        """
        Loads and returns the 'commands' key from commands.json if available.
        Returns None if the file is missing, corrupt, or does not contain 'commands'.
        """
        try:
            with open(from_root("config/commands.json"), "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    return data.get("commands")
                except ValueError:
                    return None
        except Exception:
            return None

    def _is_index_in_range(self, data, index: int) -> bool:
        """
        Checks if `index` is within the bounds of `data`.
        Returns True if index is valid, False if out of range.
        """
        try:
            _ = data[index]
            return True
        except IndexError:
            return False

    def _wrap_string_with_underscore(self, text: str) -> str:
        """
        Returns the input text in lowercase.
        (Previously used for special underscore logic; customize if needed.)
        """
        return text.lower()

    def process_syntax(self, syntax: str) -> list:
        """
        Removes any recognized prefix (e.g., "!", ".", "?", "/", ">") and splits
        the resulting command by spaces.
        """
        matched_prefix = next(
            (prefix for prefix in self.command_prefixes if syntax.startswith(prefix)),
            None,
        )
        if matched_prefix:
            syntax = syntax.replace(matched_prefix, "", 1).strip()
        return syntax.split()

    def percentage_exact_match(self, arr1: list, arr2: list) -> float:
        """
        Returns 100.0 if arr1 == arr2, else 0.0 if they differ in any element count.
        If partial exact matches are needed, the code tries to match index by index.
        """
        unique_arr1 = [x for x in arr1 if x not in arr2]
        unique_arr2 = [x for x in arr2 if x not in arr1]

        if len(unique_arr1) == 0 and len(unique_arr2) == 0:
            # Perfect match or both are empty
            return 100.0
        elif len(unique_arr1) > 0 or len(unique_arr2) > 0:
            # They differ in some elements
            return 0.0
        else:
            # Fallback partial index-by-index check
            count = 0
            min_length = min(len(arr1), len(arr2))
            for i in range(min_length):
                if arr1[i] == arr2[i]:
                    count += 1
            return (count / min_length) * 100

    def command_args_to_string(self, args: dict = None) -> str:
        """
        Builds a human-readable string with argument placeholders for required/typed arguments.
        Example: if arg_name has type 'integer', output: "arg_name {integer}"
        """
        if not args:
            return ""
        arg_list = []
        for arg_key, arg_details in args.items():
            # If it's required or has a value, we show it in the syntax
            if arg_details and "hasValue" in arg_details and "required" in arg_details:
                if arg_details["hasValue"] or arg_details["required"]:
                    arg_type = arg_details.get("type")
                    if arg_type:
                        arg_list.append(f"{arg_key} {{{arg_type}}}")
                    else:
                        # Fallback to using the arg_key as placeholder
                        arg_list.append(f"{arg_key} {{{arg_key}}}")
        return " ".join(arg_list)

    def find_matching_command(self, input_command: str = "", commands: dict = None):
        """
        Attempts to find the best matching command in 'commands' based on the highest
        percentage of exact match for the syntax.
        """
        input_command = input_command.lower()
        command_matches = []

        if input_command and commands:
            for command_name, command_details in commands.items():
                syntax = command_details["syntax"].lower()
                input_syntax = input_command.split()
                syntax_to_list = syntax.split()

                # Truncate input_syntax to the length of syntax_to_list
                if len(input_syntax) > len(syntax_to_list):
                    input_syntax = input_syntax[: len(syntax_to_list)]

                percentage_match = self.percentage_exact_match(
                    input_syntax, syntax_to_list
                )
                command_matches.append(
                    {
                        "command": command_name,
                        "percentage": percentage_match,
                        "endpoint": command_details["syntax"],
                    }
                )

            if command_matches:
                highest_percentage = max(command_matches, key=lambda x: x["percentage"])
                if highest_percentage["percentage"] > 80.0:
                    return highest_percentage["command"]
        return None

    # --- Data Type Conversions ---
    def convert_to_integer(self, value: str):
        try:
            return int(value)
        except ValueError:
            return None

    def convert_to_float(self, value: str):
        try:
            return float(value)
        except ValueError:
            return None

    def convert_to_boolean(self, value: str):
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        return None

    def convert_data_types(self, lst: list) -> list:
        """
        Convert strings in a list to int or float if possible; otherwise leave as string.
        """
        converted_list = []
        for item in lst:
            if isinstance(item, str):
                try:
                    converted_item = int(item)
                except ValueError:
                    try:
                        converted_item = float(item)
                    except ValueError:
                        converted_item = item
                converted_list.append(converted_item)
            else:
                converted_list.append(item)
        return converted_list

    # ----------------------------------------------------------------
    # UPDATED validate_arguments WITH UNKNOWN ARG PAIRS
    # ----------------------------------------------------------------
    def validate_arguments(
        self, command_input: str, arguments: dict, command_syntax: str
    ):
        """
        Validates required and optional arguments from command_input against
        the config in 'arguments'. Returns (status_bool, errors_list, collected_args).

        Additionally:
          - If a token is NOT in 'arguments', we treat it as a custom <key>,
            and if possible, consume the next token as <value>.
            Otherwise, store None if the next token is recognized or doesn't exist.

        Steps:
          1. Parse the entire input, collecting recognized arguments (required or optional).
             - For recognized arguments, we do type checks, hasValue, etc.
          2. If a token is unknown, treat it as a <key> <value> pair if the next token
             is also unknown or doesn't exist.
          3. Verify all required arguments are present.
          4. Return overall status, list of errors, and final argument-values dict.
        """
        # If there's no arguments config, or no command input, bail out
        if not command_input:
            # If user provided no input, but there might be required arguments
            if arguments:
                # We'll skip to the "did we find required arguments" check
                return self._check_missing_required(arguments)
            else:
                # No arguments and no user input, so trivially valid
                return True, [], {}

        if not arguments:
            # No arguments declared, we only parse unknown arguments as pairs
            return self._parse_unknown_arguments(command_input)

        # Split and remove empty strings
        input_tokens = [tok.strip() for tok in command_input.split() if tok.strip()]
        errors = []
        status = True

        # Holds final validated values for recognized & unknown arguments
        collected_args = {}
        i = 0

        while i < len(input_tokens):
            token = input_tokens[i]

            if token in arguments:
                # --- RECOGNIZED ARGUMENT ---
                arg_cfg = arguments[token]
                arg_name = token

                # Does this argument expect a value?
                has_value = arg_cfg.get("hasValue", False) in [True, "true"]
                arg_val = None

                if has_value:
                    # Need a value after this token
                    if (i + 1) < len(input_tokens):
                        potential_value = input_tokens[i + 1]
                        if potential_value in arguments:
                            # Next token is also an argument key -> missing value
                            errors.append(
                                f"Argument '{arg_name}' requires a value, but none provided."
                            )
                            status = False
                        else:
                            arg_val = potential_value
                            i += 1  # consume the value
                    else:
                        # No tokens left for the value
                        errors.append(
                            f"Argument '{arg_name}' is missing its required value."
                        )
                        status = False
                else:
                    # If has_value == False, treat it as a flag
                    arg_val = None

                # Validate recognized argument
                if arg_val is not None:
                    # minLength / maxLength
                    min_len = arg_cfg.get("minLength")
                    max_len = arg_cfg.get("maxLength")

                    if min_len is not None and len(arg_val) < min_len:
                        errors.append(
                            f"Argument '{arg_name}' is too short. Minimum length is {min_len}."
                        )
                        status = False

                    if max_len is not None and len(arg_val) > max_len:
                        errors.append(
                            f"Argument '{arg_name}' is too long. Maximum length is {max_len}."
                        )
                        status = False

                    # Type checks
                    arg_type = arg_cfg.get("type", "string")
                    if arg_type == "boolean":
                        converted_val = self.convert_to_boolean(arg_val)
                        if converted_val is None:
                            errors.append(
                                f"Argument '{arg_name}' must be a boolean (true/false)."
                            )
                            status = False
                        else:
                            collected_args[arg_name] = converted_val

                    elif arg_type == "integer":
                        converted_val = self.convert_to_integer(arg_val)
                        if converted_val is None:
                            errors.append(f"Argument '{arg_name}' must be an integer.")
                            status = False
                        else:
                            collected_args[arg_name] = converted_val

                    elif arg_type == "float":
                        converted_val = self.convert_to_float(arg_val)
                        if converted_val is None:
                            errors.append(f"Argument '{arg_name}' must be a float.")
                            status = False
                        else:
                            collected_args[arg_name] = converted_val

                    elif arg_type == "array":
                        accepts = arg_cfg.get("accepts", [])
                        if accepts and arg_val not in accepts:
                            errors.append(
                                f"Argument '{arg_name}' must be one of {accepts}."
                            )
                            status = False
                        else:
                            collected_args[arg_name] = arg_val
                    else:
                        # Default to string (lowercase)
                        collected_args[arg_name] = arg_val.lower()
                else:
                    # If has_value == False or we had an error reading a value
                    if not has_value:
                        # For "flag"-style arguments, store True
                        collected_args[arg_name] = True
                    # Otherwise, the error was already appended

            else:
                # --- UNKNOWN ARGUMENT ---
                key = token
                value = None

                # Look ahead to see if next token is also unknown
                if (i + 1) < len(input_tokens):
                    next_token = input_tokens[i + 1]
                    if next_token not in arguments:
                        # Use next token as the value
                        value = next_token
                        i += 1  # consume the next token as a value

                # Place the unknown pair (or single token with None)
                collected_args[key] = value

            i += 1  # Move to the next token

        # After we've processed all tokens, ensure required arguments are present
        for arg_key, arg_cfg in arguments.items():
            if arg_cfg.get("required", False) in [True, "true"]:
                if arg_key not in collected_args:
                    errors.append(f"Required argument '{arg_key}' was not provided.")
                    status = False

        return status, errors, collected_args

    # -------------- HELPER METHODS FOR validate_arguments() --------------

    def _check_missing_required(self, arguments: dict):
        """
        If user provided no input, but we have some arguments,
        check if any are required. If so, fail. Otherwise, pass.
        """
        errors = []
        status = True
        for arg_key, arg_cfg in arguments.items():
            if arg_cfg.get("required", False) in [True, "true"]:
                errors.append(f"Required argument '{arg_key}' was not provided.")
                status = False
        return status, errors, {}

    def _parse_unknown_arguments(self, command_input: str):
        """
        If there are no known arguments, simply parse everything in pairs.
        Example: "foo bar baz" -> { 'foo': 'bar', 'baz': None }
        """
        input_tokens = command_input.split()
        collected_args = {}
        i = 0
        while i < len(input_tokens):
            key = input_tokens[i]
            value = None
            if (i + 1) < len(input_tokens):
                value = input_tokens[i + 1]
                i += 1
            collected_args[key] = value
            i += 1

        # No 'required' arguments to check if no arguments are defined
        return True, [], collected_args

    # ----------------------------------------------------------------
    # The rest of the code is unchanged
    # ----------------------------------------------------------------
    def seek_commands(self, commands: dict):
        """
        Tries to find a matching command in 'commands' for self.input and
        validate that command's arguments. Returns a dict with command info.
        """
        matching_command = self.find_matching_command(self.input, commands)
        if not matching_command:
            return {
                "status": False,
                "error": "Command not found. Please check the command line helper.",
                "code": 404,
            }

        # Found a command; gather relevant command details
        command_data = commands[matching_command]
        syntax = command_data["syntax"]
        desc = command_data["description"]
        file_path = command_data["filePath"]
        authorization = command_data["authorization"]
        has_value = command_data.get("hasValue", False)
        arguments = command_data.get("arguments", {})
        is_slash = command_data.get("slashCommand", False)
        middlewares = command_data.get("middlewares", [])

        path_explode = file_path.split("/")
        name = path_explode[-1].replace(".py", "")

        # Build extended syntax with typed arguments
        syntax_args = self.command_args_to_string(arguments)
        command_syntax = f"{syntax} {syntax_args}".strip()

        # Always call validate_arguments (now handles unknown pairs too)
        status, errors, args = self.validate_arguments(self.input, arguments, syntax)

        if status and not errors:
            return {
                "status": True,
                "code": 200,
                "name": name,
                "description": desc,
                "file": file_path,
                "authorization": authorization,
                "syntax": command_syntax,
                "args": self.pair_tokens(args),
                "hasValue": has_value,
                "middlewares": middlewares,
                "slashCommand": is_slash,
            }
        else:
            return {
                "status": status,
                "code": 200,  # Possibly use 400 or 422 if invalid
                "name": name,
                "description": desc,
                "file": file_path,
                "authorization": authorization,
                "args": None,
                "syntax": command_syntax,
                "errors": errors,
                "hasValue": has_value,
                "middlewares": middlewares,
                "slashCommand": is_slash,
            }

    def pull_commands_in_same_array(
        self, commands: dict = None, data: list = None
    ) -> list:
        """
        Recursively traverses nested commands, flattening them all into a single list.
        """
        if not commands:
            commands = self.commands_list
        if data is None:
            data = []
        if not commands:
            return data

        for cmd_key, cmd_info in commands.items():
            if "commands" in cmd_info and cmd_info["commands"]:
                nested_data = self.pull_commands_in_same_array(cmd_info["commands"])
                data.extend(nested_data)
            else:
                name = self.camelcase_to_uppercase(cmd_key)
                syntax = cmd_info.get("syntax", "")
                desc = cmd_info.get("description", "")
                authorization = cmd_info.get("authorization")
                arguments = cmd_info.get("arguments", {})
                file_path = cmd_info.get("filePath", "")
                has_value = cmd_info.get("hasValue", False)
                is_slash = cmd_info.get("slashCommand", False)
                middlewares = cmd_info.get("middlewares", [])

                syntax_args = self.command_args_to_string(arguments)
                command_syntax = f"{syntax} {syntax_args}".strip()

                data.append(
                    {
                        "name": name,
                        "command": command_syntax,
                        "desc": desc,
                        "authorization": authorization,
                        "arguments": arguments,
                        "file": file_path,
                        "hasValue": has_value,
                        "slashCommand": is_slash,
                        "middlewares": middlewares,
                    }
                )
        return data

    def check_args_integrity(self, arguments: dict = None):
        """
        Checks if each argument's config has required keys (e.g., 'required', 'hasValue'),
        and if optional keys have valid data types (e.g., minLength, maxLength).
        """
        status = True
        errors = []

        if arguments:
            for argument_key, argument_value in arguments.items():
                if "required" not in argument_value:
                    errors.append(
                        f"Argument '{argument_key}' is missing ['required'] key."
                    )
                    status = False
                else:
                    if argument_value["required"] not in (True, False, "true", "false"):
                        errors.append(
                            f"Argument '{argument_key}' ['required'] must be a boolean."
                        )
                        status = False

                if "hasValue" not in argument_value:
                    errors.append(
                        f"Argument '{argument_key}' is missing ['hasValue'] key."
                    )
                    status = False
                else:
                    if argument_value["hasValue"] not in (True, False, "true", "false"):
                        errors.append(
                            f"Argument '{argument_key}' ['hasValue'] must be a boolean."
                        )
                        status = False

                if "minLength" in argument_value:
                    if not isinstance(argument_value["minLength"], int):
                        errors.append(
                            f"Argument '{argument_key}' ['minLength'] must be an integer."
                        )
                        status = False

                if "maxLength" in argument_value:
                    if not isinstance(argument_value["maxLength"], int):
                        errors.append(
                            f"Argument '{argument_key}' ['maxLength'] must be an integer."
                        )
                        status = False

                if "type" in argument_value:
                    if argument_value["type"] not in [
                        "string",
                        "boolean",
                        "integer",
                        "float",
                        "array",
                    ]:
                        errors.append(
                            f"Argument '{argument_key}' ['type'] must be one of "
                            "[string, boolean, integer, float, array]."
                        )
                        status = False

        return errors, status

    def check_commands_integrity(self, commands: dict = None, data: list = None):
        """
        Checks if each command has the required keys and if arguments are valid.
        Returns (errors_list, status_bool).
        """
        errors = []
        status = True

        # Flatten to get an array of all commands
        all_commands = self.pull_commands_in_same_array()

        for cmd in all_commands:
            if not cmd["command"]:
                errors.append(f"[syntax] in '{cmd['name']}' was not declared.")
                status = False

            if not cmd["desc"]:
                errors.append(
                    f"[description] in '{cmd['name']}' was not declared or empty."
                )
                status = False

            if "authorization" not in cmd:
                errors.append(f"[authorization] in '{cmd['name']}' was not declared.")
                status = False

            if cmd["slashCommand"] not in (True, False, "true", "false"):
                errors.append(
                    f"[slashCommand] in '{cmd['name']}' must be either 'true' or 'false'."
                )
                status = False

            if not cmd["file"]:
                errors.append(
                    f"[filePath] in '{cmd['name']}' was not declared or empty."
                )
                status = False

            if cmd["hasValue"] not in (True, False, "true", "false"):
                errors.append(
                    f"[hasValue] in '{cmd['name']}' must be either 'true' or 'false'."
                )
                status = False

            # Check integrity of arguments
            if cmd["arguments"]:
                arg_errors, arg_status = self.check_args_integrity(cmd["arguments"])
                if not arg_status:
                    errors.extend(arg_errors)
                    status = False

        return errors, status

    def camelcase_to_uppercase(self, camelcase_string: str) -> str:
        """
        Splits a camelCase or PascalCase string into separate capitalized words.
        Example: 'myNewCommand' -> 'My New Command'
        """
        words = re.findall(r"[A-Z]?[a-z]*", camelcase_string)
        capitalized_words = [w.capitalize() for w in words if w]
        return " ".join(capitalized_words)

    def build_command_helper(self, commands: dict = None, data: list = None) -> list:
        """
        Similar to 'pull_commands_in_same_array' but returns a slightly different format
        for building a help menu or other user-facing output.
        """
        if not commands:
            commands = self.commands_list
        if data is None:
            data = []
        if not commands:
            return data

        for cmd_key, cmd_info in commands.items():
            if "commands" in cmd_info and cmd_info["commands"]:
                nested_data = self.build_command_helper(cmd_info["commands"])
                data.extend(nested_data)
            else:
                name = self.camelcase_to_uppercase(cmd_key)
                syntax = cmd_info.get("syntax", "")
                desc = cmd_info.get("description", "")
                authorization = cmd_info.get("authorization")
                arguments = cmd_info.get("arguments", {})
                file_path = cmd_info.get("filePath", "")
                has_value = cmd_info.get("hasValue", False)
                is_slash = cmd_info.get("slashCommand", False)

                syntax_args = self.command_args_to_string(arguments)
                command_syntax = f"{syntax} {syntax_args}".strip()

                data.append(
                    {
                        "name": name,
                        "command": command_syntax,
                        "desc": desc,
                        "authorization": authorization,
                        "arguments": arguments,
                        "file": file_path,
                        "hasValue": has_value,
                        "slashCommand": is_slash,
                    }
                )

        return data

    def parse(self) -> dict:
        """
        Main entry point. Checks the integrity of all commands in the JSON, then
        attempts to find and validate a command for `self.input`.
        Returns a dict indicating success/failure and any errors.
        """
        check_errors, check_status = self.check_commands_integrity()
        if not check_status:
            # Commands structure is invalid
            return {"status": False, "error": "\n".join(check_errors)}

        commands = self.commands_list
        if not commands:
            return {"status": False, "error": "No commands found"}

        results = []
        for cmd_key, cmd_data in commands.items():
            # If sub-commands exist, handle them
            if "commands" in cmd_data and cmd_data["commands"]:
                results.append(self.seek_commands(cmd_data["commands"]))
            else:
                results.append(self.seek_commands({cmd_key: cmd_data}))

        # Find the first successful command parse
        for result in results:
            if "code" in result and result["code"] == 200:
                return result

        # If none is found
        return {
            "status": False,
            "error": "No command found. Check the command line helper.",
        }
