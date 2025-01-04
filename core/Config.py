from from_root import from_root
from core.EnvParser import EnvParser


class Config:
    def __init__(self):
        self.__env_parser: EnvParser = EnvParser(from_root(".env"))
        if self.__env_parser.get_error():
            raise Exception(
                f"There was an issue dealing with the ENV Configuration. Error: {self.__env_parser.get_error()}"
            )

    def env(self) -> EnvParser:
        return self.__env_parser
