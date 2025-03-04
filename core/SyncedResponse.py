import discord
from collections import defaultdict
import asyncio
from discord.ext.commands import Context
from core.Logger import Logger


class SyncedResponse:
    _queues = defaultdict(asyncio.Queue)  # Queue for each user-channel-origin triplet
    _processing_tasks = {}  # Track tasks per user-channel-origin
    _lock = asyncio.Lock()  # Ensure thread safety for shared state

    def __init__(self, ctx: Context, origin: str = "commands") -> None:
        self.ctx = ctx
        self.user_id = ctx.author.id
        self.channel_id = ctx.channel.id
        self.origin = origin  # Differentiate queues by origin

        self.logger = Logger("SyncedResponse").get_logger()

    async def send(self, content: any):
        queue_key = (self.user_id, self.channel_id, self.origin)
        queue = self._queues[queue_key]
        await queue.put(content)

        # Ensure only one processing task per queue
        async with self._lock:
            if queue_key not in self._processing_tasks:
                self._processing_tasks[queue_key] = asyncio.create_task(
                    self._process_queue(queue_key)
                )

    async def _process_queue(self, queue_key):
        queue = self._queues[queue_key]
        try:
            while True:
                # Process content from the queue
                next_content = await queue.get()
                try:
                    if isinstance(next_content, discord.Embed):
                        await self.ctx.channel.send(embed=next_content)
                    elif isinstance(next_content, str):
                        await self.ctx.channel.send(next_content)
                    else:
                        await self.ctx.channel.send("```No valid content provided.```")
                finally:
                    queue.task_done()

                # Break if the queue is empty
                if queue.empty():
                    break
        except Exception as e:
            print(f"Error while processing queue {queue_key}: {e}")
        finally:
            # Cleanup after processing
            async with self._lock:
                if queue_key in self._processing_tasks:
                    del self._processing_tasks[queue_key]
                # Remove the queue if it is empty
                if queue_key in self._queues and queue.empty():
                    del self._queues[queue_key]
