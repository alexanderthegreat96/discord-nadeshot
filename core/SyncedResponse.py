import discord
from collections import defaultdict
import asyncio
from discord.ext.commands import Context
from core.Logger import Logger


class SyncedResponse:
    """
    SyncedResponse ensures that responses sent by the bot to a user in a specific channel
    are processed in a synchronized, thread-safe order using asynchronous queues.

    This is critical for preventing race conditions and message disorder,
    especially when multiple commands or events respond concurrently.

    WARNING:
        **Do NOT modify this class.**
        It is responsible for maintaining order and integrity of message sending.
        Any changes could result in duplicate messages, broken queues,
        or concurrency issues affecting user experience.

        If you believe adjustments are necessary, consult the core developers first.

    Internal Design:
        - Maintains a unique queue per (user_id, channel_id, origin) tuple.
        - Ensures only one active processing task per queue.
        - Automatically cleans up after processing to manage memory usage.
    """

    _queues = defaultdict(asyncio.Queue)  # Queue for each user-channel-origin triplet
    _processing_tasks = {}  # Track tasks per user-channel-origin
    _lock = asyncio.Lock()  # Ensure thread safety for shared state

    def __init__(self, ctx: Context, origin: str = "commands") -> None:
        """
        Initialize SyncedResponse for a specific context and origin.

        Args:
            ctx (Context): The Discord command context (includes user, channel, etc.).
            origin (str, optional): A label to differentiate queue origins (e.g., 'commands', 'events').
                                    Defaults to 'commands'.
        """
        self.ctx: Context = ctx
        self.user_id: int = ctx.author.id
        self.channel_id: int = ctx.channel.id
        self.origin: str = origin  # Differentiate queues by origin

        self.logger: Logger = Logger("SyncedResponse").get_logger()

    async def send(self, content: any):
        """
        Queue a message to be sent in a synchronized manner.

        Args:
            content (any): The content to send. Supports `discord.Embed` or `str`.

        Behavior:
            - Adds content to the per-user-channel-origin queue.
            - Ensures only one processing task is handling that queue at a time.
        """
        queue_key = (self.user_id, self.channel_id, self.origin)
        queue = self._queues[queue_key]
        await queue.put(content)

        # Ensure only one processing task per queue
        async with self._lock:
            if queue_key not in self._processing_tasks:
                self._processing_tasks[queue_key] = asyncio.create_task(
                    self._process_queue(queue_key)
                )

    async def _process_queue(self, queue_key: tuple):
        """
        Internal method to process items in the queue and send them in order.

        Args:
            queue_key (tuple): The key identifying the specific queue (user_id, channel_id, origin).
        """
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
