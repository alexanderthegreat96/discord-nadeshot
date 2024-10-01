import json
import re
import datetime
import os


def is_json(myjson: any) -> bool:
    """Check if a string is a valid JSON."""
    myjson = str(myjson)
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True


def is_integer(string: any) -> bool:
    """Check if a string represents an integer."""
    string = str(string)
    pattern = r"^[+-]?\d+$"
    if re.match(pattern, string):
        return True
    else:
        return False


def is_float(string: any) -> bool:
    """Check if a string represents a float."""
    string = str(string)

    pattern = r"^[+-]?\d+(\.\d+)?$"
    if re.match(pattern, string):
        return True
    else:
        return False


def is_boolean(string: any) -> bool:
    """Check if a string represents a boolean value."""
    string = str(string)
    if string in ["true", "True", "false", "False"]:
        return True
    return False


def is_datetime(input_string: any, datetime_format: str = "%Y-%m-%d %H:%M:%S") -> bool:
    """Check if a string represents a datetime with the specified format."""
    try:
        input_string = str(input_string)
        datetime.datetime.strptime(input_string, datetime_format)
        return True
    except ValueError:
        return False


def is_list(value: any) -> bool:
    # Try converting a string representation of a list, e.g., "[1, 2, 3]"
    try:
        value = str(value)
        eval_value = eval(value)
        return isinstance(eval_value, list)
    except:
        return False


str


def is_dict(value: any) -> bool:
    # Try converting a string representation of a dict, e.g., '{"key": "value"}'
    try:
        value = str(value)
        eval_value = eval(value)
        return isinstance(eval_value, dict)
    except:
        return False


def is_tuple(value: any) -> bool:
    # Try converting a string representation of a tuple, e.g., "(1, 2, 3)"
    try:
        value = str(value)
        eval_value = eval(value)
        return isinstance(eval_value, tuple)
    except:
        return False


def convert_input_to_type(input_string: any = None) -> any:
    """Convert a string to the appropriate type (int, float, boolean, datetime, or str)."""
    if input_string:
        try:
            if is_integer(input_string):
                return int(input_string)

            if is_float(input_string):
                return float(input_string)

            if is_boolean(input_string):
                return True if input_string.lower() == "true" else False

            if is_datetime(input_string):
                return datetime.strptime(input_string, "%Y-%m-%d %H:%M:%S")

            if is_list(input_string):
                return eval(input_string)

            if is_tuple(input_string):
                return eval(input_string)

            if is_dict(input_string):
                return eval(input_string)

            return str(input_string)

        except ValueError:
            return input_string
    return None


def parse_env_file(file_path):
    """Parse a .env file and return its contents as a dictionary."""
    env_dict = {}

    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                key, value = line.split("=", 1)
                value = value.strip()

                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1].replace('\\"', '"')
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1].replace("\\'", "'")

                value = os.path.expandvars(value)
                env_dict[key.strip()] = value

    except FileNotFoundError as e:
        return {"status": False, "error": "Error handling file: " + str(e)}

    return {"status": True, "env": env_dict}


def convert_to_specific_type(what: any, type: str):
    """
    Converts a given value (`what`) to a specific type defined by the `type` parameter.

    This function takes a value in any form and attempts to convert it into one of the
    allowed types, which include `str`, `bool`, `float`, `int`, `list`, `tuple`, and `dict`.
    It checks if the requested type is allowed, and if so, uses pattern matching to perform
    the conversion. Additionally, the function supports parsing string representations of
    lists, dictionaries, and tuples using `eval`.

    Parameters:
    ----------
    what : any
        The value to be converted. It can be of any type (string, number, boolean, etc.).
    type : str
        A string representing the type to convert `what` to. The allowed types are:
        - 'str', 'string'
        - 'bool', 'boolean'
        - 'float'
        - 'int', 'integer'
        - 'list', 'array'
        - 'tuple'
        - 'dict', 'map'

    Returns:
    -------
    result : any
        The converted value, or `None` if the conversion failed or the type is not allowed.

    Allowed Types:
    --------------
    - 'str' or 'string' : Converts `what` to a string.
    - 'bool' or 'boolean' : Converts `what` to a boolean. Accepts "true" or "false" (case-insensitive).
    - 'float' : Converts `what` to a float, if possible.
    - 'int' or 'integer' : Converts `what` to an integer, if possible.
    - 'list' or 'array' : Attempts to evaluate and convert a string representation of a list.
    - 'tuple' : Attempts to evaluate and convert a string representation of a tuple.
    - 'dict' or 'map' : Attempts to evaluate and convert a string representation of a dictionary.

    Notes:
    ------
    - The function uses helper functions `is_boolean()`, `is_float()`, `is_integer()`, `is_list()`,
      `is_tuple()`, and `is_dict()` to validate whether `what` can be converted to the requested type.
    - For `list`, `tuple`, and `dict`, the function uses Python's `eval()` to parse the string into the respective type.
    - If the type is not in the allowed list, the function returns `None`.
    - If `what` cannot be converted to the desired type (e.g., a malformed string for a list), the function returns `None`.

    Examples:
    ---------
    >>> convert_to_specific_type("123", "int")
    123

    >>> convert_to_specific_type("true", "bool")
    True

    >>> convert_to_specific_type("[1, 2, 3]", "list")
    [1, 2, 3]

    >>> convert_to_specific_type("(1, 2, 3)", "tuple")
    (1, 2, 3)

    >>> convert_to_specific_type("{'key': 'value'}", "dict")
    {'key': 'value'}
    """

    result: any = None

    allowed_types = [
        "str",
        "string",
        "bool",
        "boolean",
        "float",
        "int",
        "integer",
        "list",
        "array",
        "tuple",
        "dict",
        "map",
    ]

    if type in allowed_types:
        match type:
            case "str" | "string":
                result = str(what)
            case "bool" | " boolean":
                if is_boolean(what):
                    result = True if what.lower() == "true" else False
            case "float":
                if is_float(what):
                    result = float(what)
            case "int" | "integer":
                if is_integer(what):
                    result = int(what)
            case "list" | "array":
                if is_list(what):
                    result = eval(what)
            case "dict" | "map":
                if is_dict(what):
                    result = eval(what)
            case "tuple":
                if is_tuple(what):
                    result = eval(what)
    return result


class EnvParser:
    """
    A class to parse environment configuration from a file and provide access to the configuration variables.

    The `EnvParser` class reads environment variables from a specified file (default is `.env`),
    parses the file contents, and stores the environment variables in a dictionary. It also
    provides methods to retrieve values, handle errors, and manage the types of configuration variables.

    Attributes:
    -----------
    __env_file : str
        The path to the environment file to be parsed. Defaults to ".env".
    __env : dict or None
        A dictionary storing environment variables after parsing, or None if parsing failed.
    __env_error : str or None
        An error message if parsing failed, or None if there were no errors.
    __accepted_types : list
        A list of accepted types for environment variable conversion, including 'str', 'bool',
        'float', 'int', 'list', 'tuple', and 'dict'.
    """

    def __init__(self, env_file_path: str = ".env") -> None:
        """
        Initializes the EnvParser instance with the specified environment file path.

        Parameters:
        -----------
        env_file_path : str, optional
            The path to the environment file. Defaults to ".env".

        Attributes:
        -----------
        __env_file : str
            The path to the environment file.
        __env : None
            Initially set to None; will be populated with parsed environment variables.
        __env_error : None
            Initially set to None; will be populated with an error message if parsing fails.
        __accepted_types : list
            List of accepted types for conversion.
        """
        self.__env_file = env_file_path
        self.__env = None
        self.__env_error = None

        self.__parse()

        self.__accepted_types = [
            "str",
            "string",
            "bool",
            "boolean",
            "float",
            "int",
            "integer",
            "list",
            "array",
            "tuple",
            "dict",
            "map",
        ]

    def __parse(self) -> None:
        """
        Parses the environment file and initializes environment variables and error state.

        This method reads the environment file specified by `self.__env_file`, uses the
        `parse_env_file` function to parse its contents, and sets `self.__env` and
        `self.__env_error` based on the parsing result.
        """
        contents: dict = parse_env_file(self.__env_file)
        if not contents["status"]:
            self.__env_error = contents["error"]
        else:
            self.__env = contents["env"]

    def get_error(self) -> any:
        """
        Returns the error message if the environment file parsing failed.

        Returns:
        --------
        any
            The error message if parsing failed; otherwise, None.
        """
        return self.__env_error

    def get_vars(self) -> dict:
        """
        Retrieves all environment variables from the internal environment dictionary and converts their values.

        This function returns a dictionary containing all environment variables from the internal
        environment (`self.__env`). It converts each value using the `convert_input_to_type` function.
        This conversion ensures that the values are in their appropriate types as determined by the
        conversion logic.

        Returns:
        --------
        dict
            A dictionary where each key is an environment variable name and each value is the converted
            value of that environment variable. If `self.__env_error` is `True` or if there are no
            environment variables, an empty dictionary is returned.

        Notes:
        ------
        - If `self.__env_error` is `True`, indicating an error with the environment configuration,
          the function will return an empty dictionary.
        - The function iterates over all key-value pairs in `self.__env` and applies `convert_input_to_type`
          to each value to convert it to the appropriate type.
        - If `self.__env` is empty, an empty dictionary is returned.

        Examples:
        ---------
        >>> self.get_vars()
        {'DATABASE_URL': 'postgres://user:password@localhost/dbname',
         'DEBUG_MODE': True,
         'MAX_CONNECTIONS': 10}
        """
        env: dict = {}
        if not self.__env_error and len(self.__env) > 0:
            for key, value in self.__env.items():
                env[key] = convert_input_to_type(value)

        return env

    def get(self, which: str, kind: str = None, default: any = None) -> any:
        """
        Retrieves a value from the environment configuration and converts it to the desired type.

        This function fetches a value from the internal environment dictionary (`self.__env`),
        which holds configuration variables. If the key (`which`) exists in the environment,
        the function attempts to retrieve it and convert it to the specified `kind`. If the
        key does not exist, it returns the provided `default` value.

        The function uses the `convert_to_specific_type` helper to handle type conversion for
        allowed types such as `str`, `int`, `float`, `bool`, `list`, etc.

        Parameters:
        -----------
        which : str
            The key to look up in the environment dictionary. This is the name of the configuration
            variable you want to retrieve.

        kind : str, optional
            A string representing the type to convert the value to. Defaults to None.
            If not provided, it will figure out the type automatically
            Accepted types include:
            - 'str', 'string'
            - 'bool', 'boolean'
            - 'float'
            - 'int', 'integer'
            - 'list', 'array'
            - 'tuple'
            - 'dict', 'map'

        default : any, optional
            The value to return if the key is not found in the environment dictionary. Defaults to `None`.

        Returns:
        --------
        any
            The value retrieved from the environment, converted to the specified `kind` if found,
            or the `default` value if the key doesn't exist. If the type conversion fails, `None`
            is returned.

        Notes:
        ------
        - If `self.__env_error` is `True`, indicating a problem with the environment configuration,
          the function will return `None`.
        - The function first checks if the key exists in the environment. If not found, it falls
          back to the `default` value.
        - If `kind` is specified and is in `self.__accepted_types`, the function converts the value
          using `convert_to_specific_type()`.
        - If the value cannot be found or the conversion fails, `None` is returned.

        Examples:
        ---------
        >>> self.get("DATABASE_URL")
        'postgres://user:password@localhost/dbname'

        >>> self.get("DEBUG_MODE", kind="bool")
        True

        >>> self.get("MAX_CONNECTIONS", kind="int", default=10)
        10

        >>> self.get("NON_EXISTENT_KEY", default="default_value")
        'default_value'
        """
        returned_value: any = None
        if not self.__env_error:
            found_value: any = None
            if which in self.__env:
                found_value = self.__env[which]
            else:
                found_value = default

            if kind and kind in self.__accepted_types:
                returned_value = (
                    convert_to_specific_type(found_value, kind) if found_value else None
                )
            else:
                returned_value: any = (
                    convert_input_to_type(found_value) if found_value else None
                )
        return returned_value
