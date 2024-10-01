import logging

# ANSI color codes for terminal output
RESET = "\033[0m"
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = (
    "\033[30m",
    "\033[31m",
    "\033[32m",
    "\033[33m",
    "\033[34m",
    "\033[35m",
    "\033[36m",
    "\033[37m",
)

SUCCESS_LEVEL_NUM = 25
logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")


def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kwargs)


logging.Logger.success = success


class CustomLoggingFormatter(logging.Formatter):
    LEVEL_COLORS = {
        logging.DEBUG: CYAN,
        logging.INFO: BLUE,
        SUCCESS_LEVEL_NUM: GREEN,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: MAGENTA,
    }

    def format(self, record):
        log_color = self.LEVEL_COLORS.get(record.levelno, WHITE)
        message = super().format(record)
        return f"{log_color}{message}{RESET}"


class Logger:
    def __init__(
        self,
        name: str,
        dump_logs: bool = False,
        log_file_path: str = "logs/nadeshot.log",
    ):
        """
        Initializes the Logger with a specific name, and configures it with handlers and a custom formatter.

        Parameters:
        - name (str): The name of the logger, typically `__name__`.
        - brand (str): A prefixed segment of text, typically: eg: EMAG-CSV-PRODUCER.
        - dump_logs (bool): If True, logs will also be saved to a file.
        - log_file (str): The name of the file where logs will be saved if dump_logs is True.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        formatter = CustomLoggingFormatter(
            f"{name} - %(asctime)s - %(levelname)s - %(message)s"
        )

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        if dump_logs:
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setFormatter(formatter)

        if not self.logger.hasHandlers():
            self.logger.addHandler(handler)
            if dump_logs:
                self.logger.addHandler(file_handler)

    def get_logger(self):
        """
        Returns the configured logger instance.

        Returns:
        - logging.Logger: The configured logger.
        """
        return self.logger
