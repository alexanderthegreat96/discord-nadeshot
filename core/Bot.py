# Standard library imports
import asyncio
import importlib
import importlib.util
import json
import sys
import time
import re
import traceback
import types
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from os import path
from typing import (
    Callable,
    Coroutine,
    Any,
    Dict,
    List,
    Union,
    Iterable,
)

# Third-party library imports
import discord
from discord.ext import commands, tasks
from from_root import from_root

# Local application imports
from core.Cache import Cache
from core.CommandLineArgumentParser import CommandLineArgumentParser
from core.EnvParser import EnvParser
from core.Logger import Logger
from core.MultiBotHandler import MultiBotHandler
from core.CooldownImmune import CooldownImmune
from utils.discord_user import DiscordUser
from core.ErrorHandler import ErrorHandler
from core.CommandLogger import CommandLogger


# This code has been cleaned up
# refactoed
# and improve by GPT 4o
class Bot:
    """
    Main Discord bot framework class, managing commands, tasks, events,
    and dynamic command loading.
    """

    def __init__(self) -> None:
        """
        Initialize the Bot with environment variables, config, tokens,
        prefix settings, command references, tasks, caching, etc.
        """
        self.env = EnvParser(from_root(".env"))
        self.config = self._bot_config()
        self.bot_token = self.env.get("BOT_TOKEN", default="Hahahaha")
        self.bot_name = self.env.get("BOT_NAME", default=self.config["bot-name"])
        self.command_prefixes: List[str] = ["!", ".", "?", "/", ">"]

        self.bot: commands.Bot = commands.Bot(
            command_prefix=self.command_prefixes,
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=self.config["bot-listens-to"],
                description=self.config["bot-description"],
            ),
            intents=discord.Intents.all(),
            case_insensitive=True,
        )
        # Holds the commands reference from discord.ext
        self.commands = commands

        # Holds references to scheduled tasks
        self.tasks: Dict[str, tasks.Loop] = {}

        # Redis connectivity for dealing with caching
        self.cache: Cache = Cache()

        # Manages multi-bot logic
        self.multi_bot_handler: MultiBotHandler = MultiBotHandler()

        # Standard issue logger
        self.logging: Logger = Logger(
            self.env.get("BOT_NAME", default="Nadeshot")
        ).get_logger()

        # Executor to handle parallel tasks,
        # preventing main event loop performance issues
        self.executor: ThreadPoolExecutor = ThreadPoolExecutor()

        # Response queues handler for channel concurrency control
        self.channel_queues: defaultdict[
            int, asyncio.Queue[Callable[[], Coroutine[None, None, None]]]
        ] = defaultdict(asyncio.Queue)

    # --------------------------------------------------------------------------
    # Data / Config Loading
    # --------------------------------------------------------------------------

    def _bot_config(self) -> Dict[str, Any]:
        """
        Loads the bot configuration from config/bot.json.

        Returns:
            dict: The bot configuration dictionary.
        """
        try:
            with open(from_root("config/bot.json"), "r") as f:
                data = json.load(f)
            return data["config"]
        except Exception as e:
            self.logging.error(f"Error loading bot config: {e}")
            return {}

    def parsed_command_list(self) -> Dict[str, Any]:
        """
        Loads the command list from config/commands.json.

        Returns:
            dict: The commands configuration dictionary.
        """
        try:
            with open(from_root("config/commands.json"), "r") as f:
                data = json.load(f)
            return data["commands"]
        except Exception as e:
            self.logging.error(f"Unable to load config/commands.json. Error: {e}")
            return {}

    def _task_list(self) -> Union[Dict[str, Any], None]:
        """
        Loads the scheduled tasks from config/tasks.json.

        Returns:
            dict or None: The tasks configuration dictionary or None if missing.
        """
        try:
            with open(from_root("config/tasks.json"), "r") as f:
                data = json.load(f)
            return data["tasks"] if "tasks" in data else None
        except Exception as e:
            self.logging.error(f"Unable to load config/tasks.json. Error: {e}")
            return None

    def staff_groups(self) -> Union[Dict[str, Any], None]:
        """
        Loads the staff groups from config/groups.json.

        Returns:
            dict or None: The groups configuration dictionary or None if missing.
        """
        try:
            with open(from_root("config/groups.json"), "r") as f:
                data = json.load(f)
            return data["groups"]
        except Exception as e:
            self.logging.error(f"Unable to load config/groups.json. Error: {e}")
            return None

    # --------------------------------------------------------------------------
    # General Utility Methods
    # --------------------------------------------------------------------------

    def array_merge(
        self,
        container: Union[List[Any], Dict[str, List[Any]]],
        key: str = None,
        value: Union[Any, Iterable[Any]] = None,
    ) -> None:
        """
        Merge unique values into a list or dictionary.

        If `value` is an iterable, each unique item is appended.
        Ensures no duplicate values within the target list.

        Args:
            container (Union[List[Any], Dict[str, List[Any]]]):
                The container to modify.
            key (str, optional):
                The key for a dictionary. Required if `container` is a dictionary.
            value (Union[Any, Iterable[Any]]):
                The value(s) to merge into the container.

        Raises:
            ValueError: If `key` is not provided for dictionary containers.
            TypeError: If container is neither a list nor a dictionary.
        """

        def add_unique(
            target_list: List[Any], items: Union[Any, Iterable[Any]]
        ) -> None:
            """Helper function to add unique items to a list."""
            if isinstance(items, (list, tuple, set)):
                for item in items:
                    if item not in target_list:
                        target_list.append(item)
            else:
                if items not in target_list:
                    target_list.append(items)

        if isinstance(container, dict):
            if key is None:
                raise ValueError("Key must be provided for dictionary containers.")
            if key not in container:
                container[key] = []
            add_unique(container[key], value)
        elif isinstance(container, list):
            add_unique(container, value)
        else:
            raise TypeError("Container must be either a list or a dictionary.")

    def add_to_list(
        self, existing_list: List[Any], new_items: Union[List[Any], Any]
    ) -> List[Any]:
        """
        Adds items to a list, ensures no duplicates, and returns the updated list.

        Args:
            existing_list (list): The original list to which items will be added.
            new_items (list or any): Items to add. Can be a list or a single item.

        Returns:
            list: The updated list with new items added, without duplicates.
        """
        if not isinstance(new_items, list):
            new_items = [new_items]

        for item in new_items:
            if item not in existing_list:
                existing_list.append(item)
        return existing_list

    def filter_list(
        self, base_list: List[Any], items_to_remove: List[Any]
    ) -> List[Any]:
        """
        Removes items from the base list if they are found in the items_to_remove list.

        Args:
            base_list (list): The list of items to filter.
            items_to_remove (list): The list of items to be removed.

        Returns:
            list: A filtered list with specified items removed.
        """
        return [item for item in base_list if item not in items_to_remove]

    def get_command_prefix_from_message(self, ctx: commands.Context) -> str:
        """
        Attempts to extract the command prefix (first character) from
        the context's message content. Falls back to '/' if no message
        is found.

        Args:
            ctx (commands.Context): The command invocation context.

        Returns:
            str: The prefix character or '/'.
        """
        if not ctx or not ctx.message:
            return "/"

        message_content: str = ctx.message.content
        return message_content[0] if message_content else "/"

    def to_camel_case(self, input_string: str) -> str:
        """
        Converts a string with dashes, underscores, or dots into CamelCase.

        Args:
            input_string (str): The string to convert.

        Returns:
            str: The CamelCase version of the input string.
        """
        parts = re.split(r"[-_.]", input_string)
        return "".join(part.capitalize() for part in parts)

    async def reply_with(self, ctx: commands.Context, content: any):
        """
        Sends a reply to the current context channel based on the type of content provided.

        :param content: The content to send. It can be:
                        - discord.Embed: to send an embed message.
                        - str: to send a plain text message.
                        - any other type: to send a default fallback message.
        """
        if isinstance(content, discord.Embed):
            await ctx.channel.send(embed=content)
        elif isinstance(content, str):
            await ctx.channel.send(content)
        else:
            await ctx.channel.send("No valid content provided.")

    async def process_queue(
        self, channel_id: int, task: Callable[[], Coroutine[None, None, None]]
    ) -> None:
        """
        Adds a coroutine task to the queue for the specified channel
        and processes that queue in a FIFO manner, ensuring only one
        task is running at a time per channel.

        Args:
            channel_id (int): The ID of the channel.
            task (Callable[[], Coroutine[None, None, None]]):
                The async coroutine function to run.
        """
        queue = self.channel_queues[channel_id]
        await queue.put(task)

        while not queue.empty():
            next_task = await queue.get()
            await next_task()
            queue.task_done()

    def should_ignore_commands_from_variants(self, server_id: int) -> bool:
        """
        Determines if commands should be ignored on a server due to
        multiple bot variants.

        Args:
            server_id (int): The guild's ID.

        Returns:
            bool: True if commands should be ignored, False otherwise.
        """
        if self.config.get("enable-multiple-bots"):
            return self.multi_bot_handler.should_ignore_commands(server_id)
        return False

    def check_if_item_is_not_empty(self, item: Any) -> bool:
        """
        Checks if an item is not None or an empty string.

        Args:
            item (Any): The item to check.

        Returns:
            bool: True if item is not empty, False otherwise.
        """
        if item is not None and item != "":
            return True
        return False

    # --------------------------------------------------------------------------
    # Task Scheduling & Management
    # --------------------------------------------------------------------------

    def get_task_schedule_message(
            self,
            hours: int,
            minutes: int,
            seconds: int,
            last_ran_at: str | None = None,      # ← NEW (ISO‑8601 UTC or None)
    ) -> str:
        """
        Return a human‑readable description of the task interval **and**
        the timestamp for the next execution (UTC).

        Example:
            "Runs every 30 m, next run at 2025‑04‑22 13:45:02 UTC (in 12 m 5 s)."
        """
        # ------------------------------------------------------------
        # 1. Build the frequency part  (unchanged logic, compacted)
        # ------------------------------------------------------------
        if hours == minutes == seconds == 0:
            freq = "Runs continuously."
        else:
            parts = []
            if hours:
                parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
            if minutes:
                parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
            if seconds:
                parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
            freq = "Runs every " + ", ".join(parts[:-1]) + (
                "" if len(parts) < 2 else ", and "
            ) + parts[-1] + "."

        # ------------------------------------------------------------
        # 2. Compute next‑run based on last_ran_at   (if provided)
        # ------------------------------------------------------------
        interval = hours * 3600 + minutes * 60 + seconds
        if not interval or not last_ran_at:
            # Fire immediately / continuously – no need for a next‑run clause
            return freq

        try:
            # Accept both "...Z" or "+00:00"
            last_dt = datetime.fromisoformat(last_ran_at.replace("Z", "+00:00"))
        except Exception:
            return f"{freq} (cannot parse last_ran_at)"

        next_run = last_dt + timedelta(seconds=interval)
        now = datetime.now(timezone.utc)

        if next_run <= now:
            return f"{freq} Next run: immediately."

        remaining = next_run - now
        hrs, rem = divmod(int(remaining.total_seconds()), 3600)
        mins, secs = divmod(rem, 60)
        pretty_delta = (
                (f"{hrs} h " if hrs else "")
                + (f"{mins} m " if mins else "")
                + (f"{secs} s" if secs or (not hrs and not mins) else "")
        ).strip()

        next_iso = next_run.strftime("%Y‑%m‑%d %H:%M:%S UTC")
        return f"{freq} Next run at {next_iso} (in {pretty_delta})."

    def add_tasks(self, task_name: str) -> None:
        """
        Adds a scheduled task by name, honouring the new
        `last_ran_at` field so a task is not re‑run sooner than
        its interval after a restart.

        Args:
            task_name (str): The name of the task to schedule.
        """
        # ------------------------------------------------------------
        # 1. Look up the task definition
        # ------------------------------------------------------------
        task_list = self._task_list()
        if not task_list or task_name not in task_list:
            self.logging.error(f"Task {task_name} not found in task list.")
            return

        task_info = task_list[task_name]
        file_name   = task_info.get("file_name")
        class_name  = task_info.get("class_name")
        seconds     = task_info.get("seconds", 0)
        minutes     = task_info.get("minutes", 0)
        hours       = task_info.get("hours", 0)
        enabled     = task_info.get("enabled", True)

        if not file_name or not class_name:
            self.logging.error(
                f"Task {task_name} error: Missing mandatory 'file_name' or 'class_name'."
            )
            return

        full_path = from_root(f"tasks/{file_name}")
        if not path.exists(full_path):
            self.logging.error(f"Task file {file_name} not found at: {full_path}")
            return

        # ------------------------------------------------------------
        # 2. Compute delay based on last_ran_at  (if any)
        # ------------------------------------------------------------
        interval = hours * 3600 + minutes * 60 + seconds
        remaining_delay = 0

        if interval and enabled:
            last_ran_raw = task_info.get("last_ran_at")
            if last_ran_raw:
                try:
                    from datetime import datetime, timezone
                    last_ran = datetime.fromisoformat(
                        last_ran_raw.replace("Z", "+00:00")
                    )
                    elapsed = (datetime.now(timezone.utc) - last_ran).total_seconds()
                    remaining_delay = max(0, interval - elapsed)
                except Exception as e:
                    self.logging.warning(
                        f"Task {task_name}: invalid last_ran_at – {e}"
                    )

        # ------------------------------------------------------------
        # 3. Register the task loop
        # ------------------------------------------------------------
        if enabled:
            try:
                self.logging.success(
                    f"Hooked Task: {task_name}. "
                    f"{self.get_task_schedule_message(hours, minutes, seconds)}"
                )

                # Import and instantiate task class
                command_contents = self.path_import(f"tasks/{file_name}")
                TaskClass = getattr(command_contents, class_name)
                task_instance = TaskClass(self.bot, self.logging)

                # ----------------------------------------
                # Per‑run wrapper to update last_ran_at
                # ----------------------------------------
                async def task_main():
                    await task_instance.main()
                    self._update_last_ran(task_name)

                def run_in_thread():
                    asyncio.run(task_main())

                # ----------------------------------------
                # Actual discord.ext.tasks loop
                # ----------------------------------------
                @tasks.loop(hours=hours, minutes=minutes, seconds=seconds)
                async def task_loop():
                    await asyncio.get_event_loop().run_in_executor(
                        self.executor, run_in_thread
                    )

                # ----------------------------------------
                # Start the loop after on_ready
                # honouring any remaining delay
                # ----------------------------------------
                @self.bot.listen()
                async def on_ready():
                    if not task_loop.is_running():
                        if remaining_delay:
                            self.logging.info(
                                f"Task {task_name}: delaying first run "
                                f"by {int(remaining_delay)} s (restart cooldown)."
                            )
                            await asyncio.sleep(remaining_delay)
                        task_loop.start()

                self.tasks[task_name] = task_loop

            except Exception as e:
                self.logging.error(f"Task {task_name} error: {e}")
        else:
            self.logging.warning(f"Skipped Task: {task_name} as it is disabled.")

    # ------------------------------------------------------------------
    # Helper to persist last_ran_at into config/tasks.json
    # ------------------------------------------------------------------
    def _update_last_ran(self, task_name: str) -> None:
        """Update (or create) the last_ran_at timestamp for a task."""
        try:
            from datetime import datetime, timezone

            tasks_cfg_path = from_root("config/tasks.json")
            with open(tasks_cfg_path, "r") as f:
                data = json.load(f)

            if "tasks" not in data or task_name not in data["tasks"]:
                # Nothing to do – config changed or task removed
                return

            ts = datetime.now(timezone.utc).isoformat()
            data["tasks"][task_name]["last_ran_at"] = ts

            # Atomic-ish write: dump to temp then replace
            tmp_path = tasks_cfg_path + ".tmp"
            with open(tmp_path, "w") as f:
                json.dump(data, f, indent=2)
            path.replace(tmp_path, tasks_cfg_path)

        except Exception as e:
            self.logging.warning(f"Task {task_name}: can't save last_ran_at – {e}")

    def shutdown_executor(self) -> None:
        """
        Shuts down the thread pool executor cleanly when the bot is stopping.
        """
        self.executor.shutdown(wait=False)

    # --------------------------------------------------------------------------
    # Dynamic Imports
    # --------------------------------------------------------------------------

    def path_import(self, absolute_path: str):
        """
        Dynamically imports a Python file by its path.

        Args:
            absolute_path (str): Relative path to the file to import.

        Returns:
            module: The imported Python module object.
        """
        spec = importlib.util.spec_from_file_location(
            absolute_path, from_root(absolute_path)
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore
        return module

    def str_to_class(self, field: str):
        """
        Dynamically retrieves a class from the sys.modules.

        Args:
            field (str): The class name as a string.

        Raises:
            NameError: If the class doesn't exist.
            TypeError: If the item is not a class.

        Returns:
            type: The retrieved class.
        """
        try:
            identifier = getattr(sys.modules[field], field)
        except AttributeError:
            raise NameError(f"{field} doesn't exist.")

        if isinstance(identifier, (types.ClassType, type)):
            return identifier
        raise TypeError(f"{field} is not a class.")

    # --------------------------------------------------------------------------
    # Middleware & Authorization
    # --------------------------------------------------------------------------

    def organize_middlewares(
        self, middlewares: List[str] = None
    ) -> Dict[str, List[str]]:
        """
        Splits an incoming list of middleware strings into 'before' and 'after'
        categories based on the prefix name: 'before_*' or 'after_*'.

        Args:
            middlewares (list, optional): List of middleware string names.

        Returns:
            dict: Dictionary with keys 'before' and 'after'.
        """
        if not middlewares:
            return {"before": [], "after": []}

        before_middlewares: List[str] = []
        after_middlewares: List[str] = []
        for middleware in middlewares:
            if middleware.startswith("before_"):
                before_middlewares.append(middleware)
            elif middleware.startswith("after_"):
                after_middlewares.append(middleware)

        return {"before": before_middlewares, "after": after_middlewares}

    def run_middleware(
        self,
        ctx: commands.Context,
        middlewares: List[str] = None,
        command_data: Dict[str, Any] = None,
    ) -> (bool, Union[str, None], Union[str, None]):
        """
        Executes the specified list of middleware classes in order.

        Args:
            ctx (commands.Context): The command invocation context.
            middlewares (list, optional): List of middleware names to be run.
            command_data (dict, optional): Data relevant to the command
                (arguments, authorization, etc.).

        Returns:
            tuple: (status, error, message)
                - status (bool): Overall success/failure of all middlewares.
                - error (str or None): If failure occurred, the error message.
                - message (str or None): A success or user feedback message.
        """
        status = True
        error = None
        message = None

        if not middlewares:
            return status, error, message

        for middleware in middlewares:
            file_path = from_root(f"middlewares/{middleware}.py")
            if path.exists(file_path):
                command_contents = self.path_import(f"middlewares/{middleware}.py")
                class_obj = getattr(command_contents, self.to_camel_case(middleware))
                run = class_obj(ctx, command_data)
                output = run.main()

                if "status" in output and not output["status"]:
                    return False, output["error"], message

                if "message" in output:
                    message = output["message"]

        return status, error, message

    def authorize(self, ctx: commands.Context, groups: List[str] = None) -> bool:
        """
        Authorizes a user against a list of authorization groups.

        Args:
            ctx (commands.Context): The context of the command invocation.
            groups (list, optional): The list of authorization groups.

        Returns:
            bool: True if authorized, False otherwise.
        """
        if not groups:
            return True

        user_info = DiscordUser(ctx)
        for group in groups:
            file_path = from_root(f"authorization/{group}.py")
            if path.exists(file_path):
                command_contents = self.path_import(f"authorization/{group}.py")
                class_obj = getattr(command_contents, self.to_camel_case(group))
                run = class_obj(ctx, user_info.user_id)
                if not run.main():
                    return False
        return True

    # --------------------------------------------------------------------------
    # Command Registration & Event Handlers
    # --------------------------------------------------------------------------

    def add_commands(self, command_name: str = "dth") -> None:
        """
        Dynamically registers a command and sets up event listeners
        for common Discord bot events.

        Args:
            command_name (str, optional):
                The primary command name. Defaults to "dth".
        """
        self.logging.success(f"Hooked Command: {command_name}")

        @self.bot.before_invoke
        async def reset_cooldown(ctx):
            """
            If a user is marked as immune from cooldown (via
            `CooldownImmune`), reset their command cooldown timer.
            """
            if self.config.get("enable-reset-cooldowns"):
                user_info = DiscordUser(ctx)
                immune = CooldownImmune(ctx, user_info.user_id)
                if immune.main():
                    return ctx.command.reset_cooldown(ctx)

        @self.bot.event
        async def on_command_error(ctx, error):
            """
            Global error handler for command execution.
            """
            if isinstance(error, commands.CommandOnCooldown):
                seconds = error.retry_after
                await ctx.send(
                    f"Your ability is on cooldown, retry in: "
                    f"<t:{int(time.time() + seconds)}:R>",
                    delete_after=seconds,
                )
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(
                    "```No command arguments provided!\n"
                    "Check the command helper for the list of commands.```"
                )
            elif isinstance(error, commands.MissingPermissions):
                await ctx.send(
                    "```You do not have permissions to execute this command or "
                    "this channel does not allow it.```"
                )
            elif isinstance(error, commands.CommandNotFound):
                # Optional to respond to unknown commands
                return
            else:
                error_trace = "".join(
                    traceback.format_exception(type(error), error, error.__traceback__)
                )
                err_handler = ErrorHandler(ctx, str(error), error_trace, self.logging)
                await err_handler.main()
                await ctx.send(
                    f"```{self.config['bot-name']} ran into a problem. "
                    "Try again and if the issue persists, contact the developer.```"
                )

        @self.bot.event
        async def on_guild_join(guild):
            """Event for joining a new guild."""
            file_path = from_root("events/on_guild_join.py")
            if path.exists(file_path):
                event_contents = self.path_import("events/on_guild_join.py")
                class_obj = getattr(event_contents, "OnGuildJoin")
                run = class_obj(guild, self.bot)
                await run.main()

        @self.bot.event
        async def on_member_join(member):
            """Event for new member join."""
            file_path = from_root("events/on_member_join.py")
            if path.exists(file_path):
                event_contents = self.path_import("events/on_member_join.py")
                class_obj = getattr(event_contents, "OnMemberJoin")
                run = class_obj(member, self.bot)
                await run.main()

        @self.bot.event
        async def on_member_remove(member):
            """Event for member removal."""
            file_path = from_root("events/on_member_remove.py")
            if path.exists(file_path):
                event_contents = self.path_import("events/on_member_remove.py")
                class_obj = getattr(event_contents, "OnMemberRemove")
                run = class_obj(member, self.bot)
                await run.main()

        @self.bot.event
        async def on_message_edit(before, after):
            """Event when a message is edited."""
            if after.author == self.bot.user:
                return
            file_path = from_root("events/on_message_edit.py")
            if path.exists(file_path):
                event_contents = self.path_import("events/on_message_edit.py")
                class_obj = getattr(event_contents, "OnMessageEdit")
                run = class_obj(before, after, self.bot)
                await run.main()

        @self.bot.event
        async def on_message_delete(message):
            """Event when a message is deleted."""
            if message.author == self.bot.user:
                return
            file_path = from_root("events/on_message_delete.py")
            if path.exists(file_path):
                event_contents = self.path_import("events/on_message_delete.py")
                class_obj = getattr(event_contents, "OnMessageDelete")
                run = class_obj(message, self.bot)
                await run.main()

        @self.bot.event
        async def on_member_ban(guild, member):
            """Event when a member is banned."""
            ban_entry = await guild.fetch_ban(member)
            ban_reason = ban_entry.reason
            file_path = from_root("events/on_member_ban.py")
            if path.exists(file_path):
                event_contents = self.path_import("events/on_member_ban.py")
                class_obj = getattr(event_contents, "OnMemberBan")
                run = class_obj(guild, member, ban_reason, self.bot)
                await run.main()

        @self.bot.event
        async def on_member_unban(guild, member):
            """Event when a member is unbanned."""
            file_path = from_root("events/on_member_unban.py")
            if path.exists(file_path):
                event_contents = self.path_import("events/on_member_unban.py")
                class_obj = getattr(event_contents, "OnMemberUnban")
                run = class_obj(guild, member, self.bot)
                await run.main()

        @self.bot.event
        async def on_message(message):
            """Event for every new message."""
            if message.author == self.bot.user or message.author.bot:
                return  # Skip bot messages

            # If a different variant of the bot is present, ignore the message
            if message.guild and self.should_ignore_commands_from_variants(
                message.guild.id
            ):
                return

            # If message doesn't start with any known prefix, we treat
            # it as a normal message event
            if not any(message.content.startswith(p) for p in self.command_prefixes):
                file_path = from_root("events/on_message.py")
                if message.guild and path.exists(file_path):
                    event_contents = self.path_import("events/on_message.py")
                    class_obj = getattr(event_contents, "OnMessage")
                    run = class_obj(message, self.bot)
                    await run.main()

            await self.bot.process_commands(message)

        # Retrieve command detail from config
        command_list = self.parsed_command_list()
        if command_name not in command_list:
            self.logging.info(f"'{command_name}' not found in the commands config.")
            return

        # Register the top-level command with potential subcommands
        @commands.cooldown(
            1,
            self.config.get("cooldown-duration", 5),
            commands.BucketType.user,
        )
        @self.bot.command(name=command_name, pass_context=True)
        async def item(ctx, *args):
            """Main command entrypoint for '{command_name}'."""
            config_middlewares = command_list[command_name].get("middlewares", [])
            global_mw = self.organize_middlewares(config_middlewares)
            all_mw_found = {"before": [], "after": []}

            # Merge global middlewares into tracking dict
            self.array_merge(all_mw_found, "before", global_mw["before"])
            self.array_merge(all_mw_found, "after", global_mw["after"])

            # Run BEFORE global middlewares
            mw_status, mw_error, mw_message = self.run_middleware(
                ctx, global_mw["before"], command_list[command_name]
            )

            if not mw_status:
                await self.reply_with(ctx, mw_error)
                return

            if mw_message:
                await self.reply_with(ctx, mw_message)

            # If user typed 'help' as argument
            if "help" in args and self.config.get("enable-automatic-command-helper"):
                if self.config["enable-automatic-command-helper"] is True:
                    parser = CommandLineArgumentParser()
                    helper = parser.build_command_helper()

                    if helper:
                        embed = discord.Embed(
                            title=self.config["bot-name"],
                            description="Command line helper",
                            color=discord.Color.blue(),
                        )
                        embed.set_footer(text="Powered by Nadeshot BETA")

                        for h_item in helper:
                            name = h_item["name"]
                            command_str = h_item["command"]
                            desc = h_item["desc"]
                            values = desc + "\n```" + command_str + "```"
                            embed.add_field(name=name, value=values, inline=False)

                        await self.reply_with(ctx, embed)
                    return
                else:
                    prefix = self.get_command_prefix_from_message(ctx)
                    await self.reply_with(
                        ctx,
                        "```Automatic command helper is disabled "
                        "due to multi-user-type permissions.\n"
                        f"You could use [{prefix}whatever-command help]. "
                        "That's where helpers are generally stored.```",
                    )
                    return

            # If user typed something else
            provided_args_str = (
                self.get_command_prefix_from_message(ctx)
                + command_name
                + " "
                + " ".join(args)
            )
            parser = CommandLineArgumentParser(provided_args_str)
            validation = parser.parse()

            # Global command input logger
            # will allow effective input logging
            command_logger: CommandLogger = CommandLogger(self.logging, ctx, validation)
            command_logger.log()

            if not validation["status"]:
                # Show errors with an embed
                embed = discord.Embed(
                    title=self.config["bot-name"],
                    description="General information",
                    color=discord.Color.blue(),
                )
                embed.set_footer(text="Powered by Nadeshot BETA")

                if "errors" in validation:
                    embed.add_field(
                        name="Command input",
                        value=validation["name"],
                        inline=False,
                    )
                    embed.add_field(
                        name="Description",
                        value=validation["description"],
                        inline=False,
                    )
                    embed.add_field(
                        name="Example input",
                        value=validation["syntax"],
                        inline=False,
                    )

                    errors_agg = ""
                    for err in validation["errors"]:
                        errors_agg += f"```{err}```"
                    embed.add_field(name="Errors", value=errors_agg, inline=False)

                if "error" in validation:
                    embed.add_field(
                        name="Error",
                        value=validation["error"],
                        inline=False,
                    )

                await self.reply_with(ctx, embed)
                return

            # If validation passed
            input_arguments = validation["args"]
            authorization_list = validation["authorization"]
            is_authorized = True

            if authorization_list:
                is_authorized = self.authorize(ctx, authorization_list)

            if not is_authorized:
                await self.reply_with(
                    ctx, "```This command requires special authorization.```"
                )
                return

            # Merge subcommand middlewares (if any) but exclude
            # what's already run
            sub_mw = self.organize_middlewares(validation["middlewares"])
            before_mw = self.filter_list(sub_mw["before"], all_mw_found["before"])
            after_mw = self.filter_list(sub_mw["after"], all_mw_found["after"])

            # Run BEFORE subcommand middlewares
            sub_mw_status, sub_mw_error, sub_mw_message = self.run_middleware(
                ctx, before_mw, validation
            )
            if not sub_mw_status:
                await self.reply_with(ctx, sub_mw_error)
                return

            if sub_mw_message:
                await self.reply_with(ctx, sub_mw_message)

            # Finally, run the actual command logic
            try:
                command_module = self.path_import("commands/" + validation["file"])
                class_obj = getattr(command_module, validation["name"])
            except Exception as e:
                if self.config.get("development-mode"):
                    await self.reply_with(
                        ctx,
                        f"```Error importing class: {e}\n{traceback.format_exc()}```",
                    )
                else:
                    error_handler = ErrorHandler(
                        ctx, str(e), traceback.format_exc(), self.logging
                    )
                    await error_handler.main()
                    await self.reply_with(ctx, "```System Error. Contact developer```")
                return

            try:
                runner = class_obj(
                    self.bot, ctx, args, authorization_list, input_arguments
                )
                await runner.main()
            except Exception as e:
                if self.config.get("development-mode"):
                    await self.reply_with(
                        ctx, f"```Error running class: {e}\n{traceback.format_exc()}```"
                    )
                else:
                    error_handler = ErrorHandler(
                        ctx, str(e), traceback.format_exc(), self.logging
                    )
                    await error_handler.main()
                    await self.reply_with(ctx, "```System Error. Contact developer```")
                return

            # Run AFTER subcommand middlewares
            after_status, after_error, after_message = self.run_middleware(
                ctx, after_mw, validation
            )
            if not after_status:
                await self.reply_with(ctx, after_error)
            elif after_message:
                await self.reply_with(ctx, after_message)

            # Run AFTER global middlewares
            global_after_status, global_after_error, global_after_msg = (
                self.run_middleware(ctx, global_mw["after"])
            )
            if not global_after_status:
                await self.reply_with(ctx, global_after_error)
            elif global_after_msg:
                await self.reply_with(ctx, global_after_msg)

    # --------------------------------------------------------------------------
    # Main Bot Runner
    # --------------------------------------------------------------------------

    def run_bot(self) -> None:
        """
        Starts the bot using the provided bot token, handling any
        invalid-token errors.
        """
        try:
            self.logging.success(f"Bot: {self.bot_name} started running...")
            self.logging.info("Awaiting user input...")
            self.bot.run(token=self.bot_token)
        except Exception as e:
            self.logging.error(
                f"Failed to start bot with token [{self.bot_token}]. " f"Error: {e}"
            )
