#!/usr/bin/python
import click
from commands.CommandGenerator import GenerateCommand
print(r"""
 __     __   __   __   __   __                __   ___  __        __  ___     __   ___ ___         
|  \ | /__` /  ` /  \ |__) |  \ __ |\ |  /\  |  \ |__  /__` |__| /  \  |  __ |__) |__   |   /\     
|__/ | .__/ \__, \__/ |  \ |__/    | \| /~~\ |__/ |___ .__/ |  | \__/  |     |__) |___  |  /~~\ """)

@click.group()
def commands():
    pass

@click.command()
@click.option('--name',default='my-command-name',help="Specify the command name")
@click.argument('command-name')

def generate(name,command_name):
    print('Generating command name: ' + command_name)
    generator = GenerateCommand(command_name)
    generator.save_command()

commands.add_command(generate)
commands()