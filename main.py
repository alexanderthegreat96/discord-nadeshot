"""
Nadeshot Bot Entry Point

Author: alexanderdth
Maintainer: alexanderdth
License: MIT
Status: Stable
"""

__author__ = "alexanderdth"
__license__ = "MIT"
__maintainer__ = "alexanderdth"
__status__ = "stable"
__name__ = "nadeshot"

from core.Bot import Bot
from art import tprint

# Display a stylized banner using ASCII art
tprint("Nadeshot v2.0")

# Initialize the bot system
system = Bot()

# Load and register traditional (non-slash) commands
commands = system.parsed_command_list()
if commands:
    for command_name, command_data in commands.items():
        if not command_data.get("slashCommand", False):
            system.add_commands(command_name)

# Load and register background tasks
tasks = system._task_list()
if tasks:
    for task in tasks:
        system.add_tasks(task)

# Start the bot
system.run_bot()
