__author__ = "alexanderdth"

__license__ = "MIT"
__maintainer__ = "alexanderdth"
__status__ = "stable"
__name__ = "dth-nadeshot-beta"

from core.Bot import Bot

system = Bot()
commands = system.command_list()

if commands:
    for command in commands:
        is_slash_command = commands[command].get("slashCommand", False)
        if not is_slash_command:
            system.add_commands(command)

tasks = system.task_list()

if tasks:
    for task in tasks:
        system.add_tasks(task)
system.boot()
