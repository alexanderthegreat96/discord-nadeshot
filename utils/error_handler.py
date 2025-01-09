from core.Logger import Logger


class ErrorHandler:
    def __init__(
        self, message: str, error: str, traceback: str, logger: Logger
    ) -> None:
        self.message = message
        self.error = error
        self.traceback = traceback
        self.logger = logger

    async def main(self) -> None:
        # logic to log this stuff in a database or file
        # can he handled here
        self.logger.error(f"Somethin happened: {self.message} - {self.error}")
        self.logger.error(f"Error traceback: {self.traceback}")
