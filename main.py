__author__ = "alexanderdth"

__license__ = "MIT"
__maintainer__ = "alexanderdth"
__status__ = "stable"
__name__ = "nadeshot"

from core.Bot import Bot
from art import *

tprint("Nadeshot v2.0")

system = Bot()
commands = system.parsed_command_list()

if commands:
    for command in commands:
        is_slash_command = commands[command].get("slashCommand", False)
        if not is_slash_command:
            system.add_commands(command)

tasks = system._task_list()

if tasks:
    for task in tasks:
        system.add_tasks(task)
system.run_bot()
