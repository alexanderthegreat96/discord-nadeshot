from utils.config import Config
from utils.user import user
import datetime

class before_command:
    def __init__(self, ctx, command_data=None):
        self.ctx = ctx
        self.server = server(ctx)
        self.user = user(ctx)
        self.user_id = self.user.getUserId()

    def main(self):
        config = Config.bot_config
        if config:
            if 'enable-user-age' in config and config['enable-user-age'] \
                    and 'user-age-limit' in config and config['user-age-limit']:

                today = datetime.datetime.now().date()
                user_creation_date = self.ctx.author.created_at.date()
                days_old = (today - user_creation_date).days

                if days_old >= config['user-age-limit']:
                    return {'status': True}
                else:
                    return {'status': False, 'error': 'Unable to run command. Account seems fresh!'}

