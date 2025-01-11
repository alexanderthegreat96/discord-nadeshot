from discord.ext import commands


class Admin:
    def __init__(self, ctx: commands.Context, user_id: int = 0):
        self.ctx: commands.Context = ctx
        self.user_id: int = user_id

    def main(self) -> bool:
        # use whatever logic you see fit
        # you may use some model to retrieve user data as well
        return False
