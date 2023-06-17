__author__ = "alexanderdth"

__license__ = "MIT"
__maintainer__ = "alexanderdth"
__status__ = "stable"
__name__ = "dth-nadeshot-beta"

from core.Bot import Bot

system = Bot()
commands = system.command_list()

if(commands):

    for command in commands:

        if('slashCommand' not in commands[command]):
            system.add_commands(command)
        else:
            if(commands[command]['slashCommand']):
                system.add_slash_commands(command)
        # if('slashCommand' in commands[command]):
        #     if(command[command]['slashCommand']):
        #         system.add_slash_commands(command)
        # else:
        #     system.add_commands(command)
system.boot()

