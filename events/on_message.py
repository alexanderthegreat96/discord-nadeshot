from core.Logger import Logger
from utils.message_wrapper import MessageWrapper

class OnMessage:
    def __init__(self, message, bot):
        self.message = message
        self.bot = bot
        self.logger = Logger("Event: OnMessage").get_logger()

        self.message_wrapper = MessageWrapper(self.message)
        self.message_data = self.message_wrapper.get_message_info()
        

    async def main(self):
        self.logger.success(f"User: {self.message_wrapper.get_author_name()} just sent a message with the content: {self.message_data}")
