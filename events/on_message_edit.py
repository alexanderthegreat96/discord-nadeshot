from core.Logger import Logger
from utils.message_wrapper import MessageWrapper

class OnMessageEdit:
    def __init__(self, before, after, bot):
        self.before = before
        self.after = after
        self.bot = bot
        
        self.logger = Logger("Event: OnMessageEdit").get_logger()
        self.message_wrapper_before = MessageWrapper(self.before)
        self.message_wrapper_after = MessageWrapper(self.after)

    async def main(self):
        self.logger.info(f"Message: {self.message_wrapper_before.get_content()} was changed to: {self.message_wrapper_after.get_content()}")
