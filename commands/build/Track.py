import discord
import asyncio
import datetime


class Track:
    def __init__(self, bot, ctx, args, authorization, inputArguments):
        self.bot = bot
        self.ctx = ctx
        self.authorization = authorization
        self.args = args
        self.inputArguments = inputArguments


    async def main(self):
        try:
            server_info = await self.bot.fetch_guild(self.ctx.guild.id)

            today = datetime.datetime.now().date()
            server_creation_date = server_info.created_at.date()
            days_old = (today - server_creation_date).days
            if(days_old >= 60):
                print("older than 3 months")
            else:
                print("younger than 3 months")
        except Exception as e:
           print(str(e))