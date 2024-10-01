import discord
from collections import defaultdict
import asyncio

# this code segmnt is used to handle synced-responses
# in other words, when users run commands
# this will prevent embeds from overlapping
# esentially creating a producer - consumer situation


class Synced:
    _queues = defaultdict(asyncio.Queue)  # Create a queue for each user-channel pair
    _processing_tasks = {}  # Track if a processing task is running per user-channel pair

    def __init__(self, ctx) -> None:
        self.ctx = ctx
        self.user_id = ctx.author.id
        self.channel_id = ctx.channel.id

    async def send(self, content: any):
        queue = self._queues[(self.user_id, self.channel_id)]
        await queue.put(content)

        if (self.user_id, self.channel_id) not in self._processing_tasks:
            self._processing_tasks[(self.user_id, self.channel_id)] = (
                asyncio.create_task(self._process_queue())
            )

    async def _process_queue(self):
        queue = self._queues[(self.user_id, self.channel_id)]
        while not queue.empty():
            next_content = await queue.get()
            if isinstance(next_content, discord.Embed):
                await self.ctx.channel.send(embed=next_content)
            elif isinstance(next_content, str):
                await self.ctx.channel.send(next_content)
            else:
                await self.ctx.channel.send("```No valid content provided.```")

            await asyncio.sleep(0.2)
        del self._processing_tasks[(self.user_id, self.channel_id)]
