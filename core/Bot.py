# Standard library imports
import asyncio
import importlib
import importlib.util
import json
import sys
import time
import re
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from os import path
from typing import Callable, Coroutine
import traceback
import types
from typing import Any, Dict, List, Union, Iterable

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
from utils.cooldown_immune import CooldownImmune
from utils.discord_user import DiscordUser
from utils.error_handler import ErrorHandler
from utils.synced import Synced


class Bot:
    def __init__(
        self,
    ):
        self.env = EnvParser(from_root(".env"))
        self.config = self.bot_config()
        self.bot_token = self.env.get("BOT_TOKEN", default="Hahahaha")
        self.bot_name = self.env.get("BOT_NAME", default=self.config["bot-name"])
        self.command_prefixes: list = ["!", ".", "?", "/", ">"]

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
        self.commands = commands  # holds the commands
        self.tasks: dict = {}  # holds the tasks
        self.cache: Cache = Cache()  # redis connectivity for dealing with caching
        self.multi_bot_handler: MultiBotHandler = MultiBotHandler()

        self.logging: Logger = Logger(
            self.env.get("BOT_NAME", default="Nadeshot")
        ).get_logger()  # standard issue logger

        self.executor: ThreadPoolExecutor = ThreadPoolExecutor()  # handles execution of taks in parallel to prevent main process performance issues

        # response queues handler
        self.channel_queues: defaultdict[
            int, asyncio.Queue[Callable[[], Coroutine[None, None, None]]]
        ] = defaultdict(asyncio.Queue)

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
            container (Union[List[Any], Dict[str, List[Any]]]): The container to modify.
            key (str, optional): The key for a dictionary. Required if `container` is a dictionary.
            value (Union[Any, Iterable[Any]]): The value(s) to merge into the container.

        Returns:
            None: Modifies the container in place.
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

    def add_to_list(self, existing_list: list, new_items: list):
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

    def filter_list(self, base_list: list, items_to_remove: list):
        """
        Removes items from the base list if they are found in the items_to_remove list.

        Args:
            base_list (list): The list of strings to filter.
            items_to_remove (list): The list of strings to be removed.

        Returns:
            list: A filtered list with specified items removed.
        """
        return [item for item in base_list if item not in items_to_remove]

    def get_command_prefix_from_message(self, ctx: commands.Context):
        if not ctx:
            return "/"

        message: str = ctx.message.content
        if message:
            return message[0]

        return "/"

    def to_camel_case(self, input_string: str) -> str:
        # Split the string using dashes, underscores, or dots as delimiters
        parts = re.split(r"[-_.]", input_string)
        # Capitalize each part and join them together
        return "".join(part.capitalize() for part in parts)

    # processing commands from multple users in the same channel
    # this prevents responses / events from overlapping
    async def process_queue(
        self, channel_id: int, task: Callable[[], Coroutine[None, None, None]]
    ) -> None:
        """
        Adds a task to the queue for the specified channel and processes the queue.

        Args:
            channel_id (int): The ID of the channel.
            task (Callable[[], Coroutine[None, None, None]]): The task (coroutine function) to run.
        """
        # Get the queue for the specific channel
        queue = self.channel_queues[channel_id]

        # Put the task in the queue
        await queue.put(task)

        # Ensure only one task is running at a time for each channel
        while not queue.empty():
            # Get the next task in the queue
            next_task = await queue.get()

            # Run the task (which is the coroutine function) and wait for it to finish
            await next_task()

            # Mark the task as done
            queue.task_done()

    def bot_config(self):
        try:
            f = open(from_root("config/bot.json"), "r")
            data = json.load(f)
            return data["config"]
        except Exception as e:
            self.logging.error(e)
            return None

    def staff_groups(self):
        try:
            f = open(from_root("config/groups.json"), "r")
            data = json.load(f)
            return data["groups"]
        except Exception as e:
            self.logging.error(f"Unable to load config/groups.json. Error: {e}")
            return None

    def str_to_class(self, field: str):
        try:
            identifier = getattr(sys.modules[field], field)
        except AttributeError:
            raise NameError("%s doesn't exist." % field)
        if isinstance(identifier, (types.ClassType, types.TypeType)):
            return identifier
        raise TypeError("%s is not a class." % field)

    def command_list(self) -> dict:
        try:
            f = open(from_root("config/commands.json"), "r")
            data = json.load(f)
            return data["commands"]
        except Exception as e:
            self.logging.error(f"Unable to load config/commands.json. Error: {e}")
            return None

    def should_ignore_commands_from_variants(self, server_id: int) -> bool:
        # will use redis caching to store bot status within a server
        # if a server has more than 1 variants
        # the rest should skip the commands
        config = self.bot_config()

        if config["enable-multiple-bots"]:
            return self.multi_bot_handler.should_ignore_commands(server_id)

        return False

    def task_list(self):
        try:
            f = open(from_root("config/tasks.json"), "r")
            data = json.load(f)
            return data["tasks"] if "tasks" in data else None
        except Exception as e:
            self.logging.error(f"Unable to load config/tasks.json. Error: {e}")
            return None

    def get_task_schedule_message(self, hours: int, minutes: int, seconds: int) -> str:
        """
        Generates a human-readable message about the task schedule based on hours, minutes, and seconds.

        Args:
            hours (int): Number of hours between each task run.
            minutes (int): Number of minutes between each task run.
            seconds (int): Number of seconds between each task run.

        Returns:
            str: A descriptive message about how frequently the task runs.
        """
        if hours == 0 and minutes == 0 and seconds == 0:
            return "The task will run continuously."

        if hours == 0 and minutes == 0:
            return f"The task will run every {seconds} second{'s' if seconds != 1 else ''}."

        if hours == 0 and seconds == 0:
            return f"The task will run every {minutes} minute{'s' if minutes != 1 else ''}."

        if minutes == 0 and seconds == 0:
            return f"The task will run hourly."

        if hours == 0:
            return f"The task will run every {minutes} minute{'s' if minutes != 1 else ''} and {seconds} second{'s' if seconds != 1 else ''}."

        if minutes == 0:
            return f"The task will run every {hours} hour{'s' if hours != 1 else ''} and {seconds} second{'s' if seconds != 1 else ''}."

        if seconds == 0:
            return f"The task will run every {hours} hour{'s' if hours != 1 else ''} and {minutes} minute{'s' if minutes != 1 else ''}."

        return f"The task will run every {hours} hour{'s' if hours != 1 else ''}, {minutes} minute{'s' if minutes != 1 else ''}, and {seconds} second{'s' if seconds != 1 else ''}."

    def add_tasks(self, taskname: str) -> None:
        tasklist = self.task_list()
        if tasklist and taskname in tasklist:
            task_info = tasklist[taskname]

            if "file_name" in task_info and "class_name" in task_info:
                file_name = task_info["file_name"]
                class_name = task_info["class_name"]

                seconds = task_info.get("seconds", 0)
                minutes = task_info.get("minutes", 0)
                hours = task_info.get("hours", 0)
                enabled = task_info.get("enabled", True)

                if path.exists(from_root(f"tasks/{file_name}")):
                    if enabled:
                        try:
                            self.logging.success(
                                f"Hooked Task: {taskname}. {self.get_task_schedule_message(hours, minutes, seconds)}"
                            )

                            command_contents = self.path_import(f"tasks/{file_name}")
                            TaskClass = getattr(command_contents, class_name)
                            task_instance = TaskClass(
                                self.bot,
                                self.logging,
                            )

                            async def task_main():
                                await task_instance.main()

                            def run_in_thread():
                                asyncio.run(task_main())

                            @tasks.loop(hours=hours, minutes=minutes, seconds=seconds)
                            async def task_loop():
                                await asyncio.get_event_loop().run_in_executor(
                                    self.executor, run_in_thread
                                )

                            @self.bot.listen()
                            async def on_ready():
                                if not task_loop.is_running():
                                    task_loop.start()

                            self.tasks[taskname] = task_loop
                        except Exception as e:
                            self.logging.error(f"Task {taskname} error: {e}")
                    else:
                        self.logging.warning(
                            f"Skipped Task: {taskname} as it is disabled."
                        )
                else:
                    self.logging.error(
                        f"Task {taskname} error: Missing one of the mandatory keys: file_name, class_name."
                    )
            else:
                self.logging.error(f"Task {file_name} not found in tasks/task.json")
        else:
            self.logging.error(f"Task {taskname} not found in task list.")

    def shutdown_executor(self):
        """Shutdown the executor cleanly when the bot is stopping."""
        self.executor.shutdown(wait=False)

    # imports given modules / python files allowing
    # dependency injection

    def path_import(self, absolute_path):
        spec = importlib.util.spec_from_file_location(
            absolute_path, from_root(absolute_path)
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def check_if_item_is_not_empty(self, item):
        if item is not None:
            return True
        elif item != "":
            return True
        else:
            return False

    def validate_command_inputs(self, inputs):
        if "arguments" in inputs and len(inputs["arguments"]):
            for item in inputs["arguments"]:
                self.validate_command_inputs(item)

    def organize_middlewares(self, middlewares: list = []) -> list:
        if middlewares:
            before_middlewares: list = []
            after_middlewares: list = []
            for middleware in middlewares:
                if middleware.startswith("before_"):
                    before_middlewares.append(middleware)
                elif middleware.startswith("after_"):
                    after_middlewares.append(middleware)

            return {"before": before_middlewares, "after": after_middlewares}
        return []

    def run_middleware(self, ctx, middlewares=[], command_data=None):
        status = True
        error = None
        message = None

        if middlewares:
            for middleware in middlewares:
                if path.exists(from_root(f"middlewares/{middleware}.py")):
                    commandContents = self.path_import(f"middlewares/{middleware}.py")
                    className = getattr(commandContents, self.to_camel_case(middleware))
                    run = className(ctx, command_data)
                    output = run.main()

                    if "status" in output:
                        if not output["status"]:
                            status = False
                            error = output["error"]
                            return status, error, message

                        else:
                            status = True
                            if "message" in output:
                                message = output["message"]

        return status, error, message

    def authorize(self, ctx: commands.Context, groups: list = []) -> bool:
        if groups:
            userInfo = DiscordUser(ctx)
            for group in groups:
                if path.exists(from_root(f"authorization/{group}.py")):
                    commandContents = self.path_import(f"authorization/{group}.py")
                    className = getattr(commandContents, self.to_camel_case(group))
                    run = className(ctx, userInfo.user_id)
                    return run.main()
        return True

    def __skip_strings(self, skip_strings: list = None, user_input: str = ""):
        for item in skip_strings:
            if user_input.startswith(item):
                return True
        return False

    def add_commands(self, commandName="dth"):
        self.logging.success(f"Hooked Command: {commandName}")

        @self.bot.before_invoke
        async def reset_cooldown(ctx):
            if self.config["enable-reset-cooldowns"]:
                userInfo = DiscordUser(ctx)
                immune = CooldownImmune(ctx, userInfo.user_id)
                if immune.main():
                    return ctx.command.reset_cooldown(ctx)

        @self.bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandOnCooldown):
                seconds = error.retry_after
                await ctx.send(
                    f"Your ability is on cooldown, retry in: <t:{int(time.time() + seconds)}:R>",
                    delete_after=seconds,
                )
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(
                    "```No command arguments provided! \nCheck the command helper for the list of commands.```"
                )
            elif isinstance(error, commands.MissingPermissions):
                await ctx.send(
                    "```You do not have permissions to execute this command or this channel does not allow it.```"
                )
            elif isinstance(error, commands.CommandNotFound):
                # await ctx.send("```Unknown command. Run: [/dth help] for a full list of commands.```")
                pass
            else:
                error_traceback = "".join(
                    traceback.format_exception(type(error), error, error.__traceback__)
                )
                error_handler = ErrorHandler(
                    ctx.message.content, str(error), error_traceback, self.logging
                )
                await error_handler.main()
                await ctx.send(
                    f"```{self.config['bot-name']} ran into a problem. Try again and if the issue persists, contact the developer.```"
                )

        @self.bot.event
        async def on_guild_join(guild):
            if path.exists(from_root("events/on_guild_join.py")):
                event_contents = self.path_import("events/on_guild_join.py")
                class_name = getattr(event_contents, "OnGuildJoin")
                run = class_name(guild, self.bot)
                await run.main()

        @self.bot.event
        async def on_member_join(member):
            if path.exists(from_root("events/on_member_join.py")):
                event_contents = self.path_import("events/on_member_join.py")
                class_name = getattr(event_contents, "OnMemberJoin")
                run = class_name(member, self.bot)
                await run.main()

        @self.bot.event
        async def on_member_remove(member):
            if path.exists(from_root("events/on_member_remove.py")):
                event_contents = self.path_import("events/on_member_remove.py")
                class_name = getattr(event_contents, "OnMemberRemove")
                run = class_name(member, self.bot)
                await run.main()

        @self.bot.event
        async def on_message_edit(before, after):
            if after.author == self.bot.user:
                return
            if path.exists(from_root("events/on_message_edit.py")):
                event_contents = self.path_import("events/on_message_edit.py")
                class_name = getattr(event_contents, "OnMessageEdit")
                run = class_name(before, after, self.bot)
                await run.main()

        @self.bot.event
        async def on_message_delete(message):
            if message.author == self.bot.user:
                return

            if path.exists(from_root("events/on_message_delete.py")):
                event_contents = self.path_import("events/on_message_delete.py")
                class_name = getattr(event_contents, "OnMessageDelete")
                run = class_name(message, self.bot)
                await run.main()

        @self.bot.event
        async def on_member_ban(guild, member):
            ban_entry = await guild.fetch_ban(member)
            ban_reason = ban_entry.reason

            if path.exists(from_root("events/on_member_ban.py")):
                event_contents = self.path_import("events/on_member_ban.py")
                class_name = getattr(event_contents, "OnMemberBan")
                run = class_name(guild, member, ban_reason, self.bot)
                await run.main()

        @self.bot.event
        async def on_member_unban(guild, member):
            if path.exists(from_root("events/on_member_unban.py")):
                event_contents = self.path_import("events/on_member_unban.py")
                class_name = getattr(event_contents, "OnMemberUnban")
                run = class_name(guild, member, self.bot)
                await run.main()

        @self.bot.event
        async def on_message(message):
            # skip self messages
            if message.author == self.bot.user:
                return

            # skip bot messages
            if message.author.bot:
                return

            # skip commands in normal messages
            if not any(
                message.content.startswith(prefix) for prefix in self.command_prefixes
            ):
                # if a different variant of the bot exists in the server
                # return null
                # just ignore dms
                if message.guild and message.guild.id != 0:
                    if self.should_ignore_commands_from_variants(message.guild.id):
                        return

                if message.guild and path.exists(from_root("events/on_message.py")):
                    event_contents = self.path_import("events/on_message.py")
                    class_name = getattr(event_contents, "OnMessage")
                    run = class_name(message, self.bot)
                    await run.main()

            await self.bot.process_commands(message)

        command_list = self.command_list()
        if command_list and commandName in command_list:
            if "commands" not in command_list[commandName]:
                self.logging.info(f"{commandName} has no subcommands.")

            @commands.cooldown(
                # The above code is a Python script defining a function or command using the `@command`
                # decorator. However, the actual implementation or purpose of the function is not provided
                # in the code snippet.
                1,
                self.config["cooldown-duration"],
                commands.BucketType.user,
            )
            @self.bot.command(name=commandName, pass_context=True)
            async def item(ctx, *args):
                # will use synced responses
                # to prevent message / outputs / embeds overlapping
                # this is handled on a per-user + per channel basis
                # works like a queue system
                response: Synced = Synced(ctx)

                # handle global middlewares
                all_middlewares_found: dict = {}

                if (
                    "middlewares" in command_list[commandName]
                    and command_list[commandName]["middlewares"]
                ):
                    global_middlewares = self.organize_middlewares(
                        command_list[commandName]["middlewares"]
                    )

                    # keep track of the middlewares
                    self.array_merge(
                        all_middlewares_found, "before", global_middlewares["before"]
                    )
                    self.array_merge(
                        all_middlewares_found, "after", global_middlewares["after"]
                    )

                    before: list = global_middlewares["before"]
                    after: list = global_middlewares["after"]

                    middleware_status = True
                    middleware_error = None
                    middleware_message = None

                    if before:
                        middleware_status, middleware_error, middleware_message = (
                            self.run_middleware(ctx, before, command_list[commandName])
                        )

                    if middleware_status:
                        if middleware_message:
                            await response.send(middleware_message)

                        if (
                            "help" in args
                            and self.config["enable-automatic-command-helper"]
                        ):
                            if self.config["enable-automatic-command-helper"] == True:
                                parser = CommandLineArgumentParser()
                                helper = parser.build_command_helper()

                                if helper:
                                    nadeshotEmbed = discord.Embed(
                                        title=self.config["bot-name"],
                                        description="Command line helper",
                                        color=discord.Color.blue(),
                                    )
                                    nadeshotEmbed.set_footer(
                                        text="Powered by Nadeshot BETA"
                                    )

                                    for item in helper:
                                        name = item["name"]
                                        command_str = item["command"]
                                        desc = item["desc"]
                                        authorization = item["authorization"]
                                        arguments = item["arguments"]

                                        values = (
                                            desc + "\n" + "```" + command_str + "```\n"
                                        )
                                        nadeshotEmbed.add_field(
                                            name=name, value=values, inline=False
                                        )

                                    await response.send(nadeshotEmbed)
                            else:
                                await response.send(
                                    "```Automatic command helper is disabled due to multi-user-type permissions.\n"
                                    f"You could use [{self.get_command_prefix_from_message(ctx)}whatever-command help]. That's where helpers are generally stored.```"
                                )
                        else:
                            providedArguments = (
                                self.get_command_prefix_from_message(ctx)
                                + ""
                                + commandName
                                + " "
                                + " ".join(args)
                            )

                            parser = CommandLineArgumentParser(providedArguments)
                            validation = parser.parse()

                            if validation["status"]:
                                inputArguments = validation["args"]
                                authorization = []
                                authorize = True
                                middlewares = self.organize_middlewares(
                                    validation["middlewares"]
                                )

                                if len(validation["authorization"]):
                                    authorization = validation["authorization"]
                                    authorize = self.authorize(ctx, authorization)

                                if not authorize:
                                    await response.send(
                                        "```This command requires special authorization.```"
                                    )
                                else:
                                    middleware_status = True
                                    middleware_error = None
                                    middleware_message = None

                                    before = []
                                    after = []

                                    if middlewares:
                                        before = self.filter_list(
                                            middlewares["before"],
                                            all_middlewares_found["before"],
                                        )
                                        after = self.filter_list(
                                            middlewares["after"],
                                            all_middlewares_found["after"],
                                        )

                                        if before:
                                            (
                                                middleware_status,
                                                middleware_error,
                                                middleware_message,
                                            ) = self.run_middleware(
                                                ctx, before, validation
                                            )

                                    if middleware_status:
                                        if middleware_message:
                                            await response.send(middleware_message)
                                        try:
                                            commandContents = self.path_import(
                                                "commands/" + validation["file"]
                                            )
                                            className = getattr(
                                                commandContents, validation["name"]
                                            )
                                            try:
                                                run = className(
                                                    self.bot,
                                                    ctx,
                                                    args,
                                                    authorization,
                                                    inputArguments,
                                                )
                                                await run.main()
                                            except Exception as e:
                                                if self.config["development-mode"]:
                                                    await response.send(
                                                        "```Error running class: "
                                                        + str(e)
                                                        + "\n"
                                                        + str(traceback.format_exc())
                                                        + "```"
                                                    )
                                                else:
                                                    await response.send(
                                                        "```System Error. Contact developer```"
                                                    )
                                        except Exception as e:
                                            if self.config["development-mode"]:
                                                await response.send(
                                                    "```Error importing class: "
                                                    + str(e)
                                                    + "\n"
                                                    + str(traceback.format_exc())
                                                    + "```"
                                                )
                                            else:
                                                await response.send(
                                                    "```System Error. Contact developer```"
                                                )
                                    else:
                                        await response.send(
                                            "```Error: " + middleware_error + "```"
                                        )

                                    if after:
                                        (
                                            run_after_status,
                                            run_after_error,
                                            run_after_message,
                                        ) = self.run_middleware(ctx, after, validation)
                                        if not run_after_status:
                                            await response.send(
                                                "```Error: " + run_after_error + "```"
                                            )
                                        else:
                                            if run_after_message:
                                                await response.send(run_after_message)

                            else:
                                nadeshotEmbed = discord.Embed(
                                    title=self.config["bot-name"],
                                    description="General information",
                                    color=discord.Color.blue(),
                                )
                                nadeshotEmbed.set_footer(
                                    text="Powered by Nadeshot BETA"
                                )

                                if "errors" in validation:
                                    nadeshotEmbed.add_field(
                                        name="Command input",
                                        value=validation["name"],
                                        inline=False,
                                    )
                                    nadeshotEmbed.add_field(
                                        name="Description",
                                        value=validation["description"],
                                        inline=False,
                                    )
                                    nadeshotEmbed.add_field(
                                        name="Example input",
                                        value=validation["syntax"],
                                        inline=False,
                                    )

                                    errors = ""
                                    for error in validation["errors"]:
                                        errors += "```" + error + "```"

                                    nadeshotEmbed.add_field(
                                        name="Errors", value=errors, inline=False
                                    )

                                if "error" in validation:
                                    nadeshotEmbed.add_field(
                                        name="Error",
                                        value=validation["error"],
                                        inline=False,
                                    )

                                await response.send(nadeshotEmbed)
                    else:
                        await response.send("```Error: " + middleware_error + "```")

                    if after:
                        run_after_status, run_after_error, run_after_message = (
                            self.run_middleware(ctx, after)
                        )
                        if not run_after_status:
                            await response.send("```Error: " + run_after_error + "```")
                        else:
                            if run_after_message:
                                await response.send(run_after_message)

                else:
                    # if no global middlewares are set
                    # execute the program
                    # normally

                    if (
                        "help" in args
                        and self.config["enable-automatic-command-helper"]
                    ):
                        if self.config["enable-automatic-command-helper"] == True:
                            parser = CommandLineArgumentParser()
                            helper = parser.build_command_helper()

                            if helper:
                                nadeshotEmbed = discord.Embed(
                                    title=self.config["bot-name"],
                                    description="Command line helper",
                                    color=discord.Color.blue(),
                                )
                                nadeshotEmbed.set_footer(
                                    text="Powered by Nadeshot BETA"
                                )

                                for item in helper:
                                    name = item["name"]
                                    command_str = item["command"]
                                    desc = item["desc"]
                                    authorization = item["authorization"]
                                    arguments = item["arguments"]

                                    values = desc + "\n" + "```" + command_str + "```\n"
                                    nadeshotEmbed.add_field(
                                        name=name, value=values, inline=False
                                    )

                                await response.send(nadeshotEmbed)
                        else:
                            await response.send(
                                "```Automatic command helper is disabled due to multi-user-type permissions.\n"
                                f"You could use [{self.get_command_prefix_from_message(ctx)}whatever-command help]. That's where helpers are generally stored.```"
                            )
                    else:
                        providedArguments = (
                            self.get_command_prefix_from_message(ctx)
                            + ""
                            + commandName
                            + " "
                            + " ".join(args)
                        )

                        parser = CommandLineArgumentParser(providedArguments)
                        validation = parser.parse()

                        if validation["status"]:
                            inputArguments = validation["args"]

                            authorization = []
                            authorize = True
                            middlewares = self.organize_middlewares(
                                validation["middlewares"]
                            )

                            if len(validation["authorization"]):
                                authorization = validation["authorization"]
                                authorize = self.authorize(ctx, authorization)

                            if not authorize:
                                response.send(
                                    "```This command requires special authorization.```"
                                )
                            else:
                                middleware_status = True
                                middleware_error = None
                                middleware_message = None

                                before = []
                                after = []

                                if middlewares:
                                    before = middlewares["before"]
                                    after = middlewares["after"]

                                    if before:
                                        (
                                            middleware_status,
                                            middleware_error,
                                            middleware_message,
                                        ) = self.run_middleware(ctx, before, validation)

                                if middleware_status:
                                    if middleware_message:
                                        await response.send(middleware_message)
                                    try:
                                        commandContents = self.path_import(
                                            "commands/" + validation["file"]
                                        )
                                        className = getattr(
                                            commandContents, validation["name"]
                                        )
                                        try:
                                            run = className(
                                                self.bot,
                                                ctx,
                                                args,
                                                authorization,
                                                inputArguments,
                                            )
                                            await run.main()
                                        except Exception as e:
                                            if self.config["development-mode"]:
                                                await response.send(
                                                    "```Error running class: "
                                                    + str(e)
                                                    + "\n"
                                                    + str(traceback.format_exc())
                                                    + "```"
                                                )
                                            else:
                                                await response.send(
                                                    "```System Error. Contact developer```"
                                                )
                                    except Exception as e:
                                        if self.config["development-mode"]:
                                            await response.send(
                                                "```Error importing class: "
                                                + str(e)
                                                + "\n"
                                                + str(traceback.format_exc())
                                                + "```"
                                            )
                                        else:
                                            await response.send(
                                                "```System Error. Contact developer```"
                                            )
                                else:
                                    await response.send(
                                        "```Error: " + middleware_error + "```"
                                    )

                                if after:
                                    (
                                        run_after_status,
                                        run_after_error,
                                        run_after_message,
                                    ) = self.run_middleware(ctx, after, validation)
                                    if not run_after_status:
                                        await response.send(
                                            "```Error: " + run_after_error + "```"
                                        )
                                    else:
                                        if run_after_message:
                                            await response.send(run_after_message)

                        else:
                            nadeshotEmbed = discord.Embed(
                                title=self.config["bot-name"],
                                description="General information",
                                color=discord.Color.blue(),
                            )
                            nadeshotEmbed.set_footer(text="Powered by Nadeshot BETA")

                            if "errors" in validation:
                                nadeshotEmbed.add_field(
                                    name="Command input",
                                    value=validation["name"],
                                    inline=False,
                                )
                                nadeshotEmbed.add_field(
                                    name="Description",
                                    value=validation["description"],
                                    inline=False,
                                )
                                nadeshotEmbed.add_field(
                                    name="Example input",
                                    value=validation["syntax"],
                                    inline=False,
                                )

                                errors = ""
                                for error in validation["errors"]:
                                    errors += "```" + error + "```"

                                nadeshotEmbed.add_field(
                                    name="Errors", value=errors, inline=False
                                )

                            if "error" in validation:
                                nadeshotEmbed.add_field(
                                    name="Error",
                                    value=validation["error"],
                                    inline=False,
                                )

                            await response.send(nadeshotEmbed)

    def boot(self):
        try:
            self.logging.success(f"Bot: {self.bot_name} started running...")
            self.logging.info("Awaiting user input...")
            self.bot.run(token=self.bot_token)
        except Exception as e:
            self.logging.error(
                f"Bot token: [{self.bot_token}] is invalid. Please check."
            )
