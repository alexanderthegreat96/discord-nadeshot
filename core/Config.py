from from_root import from_root
from core.EnvParser import EnvParser


class Config:
    """
    Config is a user-editable class where all additional configuration
    parameters are declared. It loads environment variables from the
    project root `.env` file using EnvParser.
    """

    def __init__(self):
        """
        Initializes the Config instance by loading the .env file from
        the project root. Raises an exception if there is an error
        during environment parsing.
        """
        self.__env_parser: EnvParser = EnvParser(from_root(".env"))
        if self.__env_parser.get_error():
            raise Exception(
                f"There was an issue dealing with the ENV Configuration. Error: {self.__env_parser.get_error()}"
            )

    def env(self) -> EnvParser:
        """
        Returns:
            EnvParser: The instance of EnvParser loaded with .env configuration.
        """
        return self.__env_parser
