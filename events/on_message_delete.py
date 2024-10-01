from core.Logger import Logger
from utils.message_wrapper import MessageWrapper

class OnMessageDelete:
    def __init__(self, message, bot):
        self.message = message
        self.bot = bot
        self.logger = Logger("Event: OnMessageDelete").get_logger()
        
        self.message_wrapper = MessageWrapper(self.message)

    async def main(self):
        self.logger.warning(f"User: {self.message_wrapper.get_author_name()} deleted message: {self.message_wrapper.get_message_info()}.")
