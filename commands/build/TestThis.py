import discord
import asyncio

class TestThis:
    def __init__(self, bot, ctx, args, authorization, inputArguments):
        self.bot = bot
        self.ctx = ctx
        self.authorization = authorization
        self.args = args
        self.inputArguments = inputArguments


    async def main(self):
        await self.ctx.channel.send("```This is the TestThis command output within commands folder.```")
                    