#!/usr/bin/python
import click
from commands.CommandGenerator import GenerateCommand
from commands.TaskGenerator import TaskGeneratorCommand

print(r"""
 __     __   __   __   __   __                __   ___  __        __  ___     __   ___ ___         
|  \ | /__` /  ` /  \ |__) |  \ __ |\ |  /\  |  \ |__  /__` |__| /  \  |  __ |__) |__   |   /\     
|__/ | .__/ \__, \__/ |  \ |__/    | \| /~~\ |__/ |___ .__/ |  | \__/  |     |__) |___  |  /~~\ """)


@click.group()
def commands():
    pass


@click.command()
@click.option(
    "--command-name", default="my-command-name", help="Specify the command name"
)
@click.option(
    "--command-prefix", default="/", help="Specifi the command prefix. Default: /"
)
@click.argument("command-name")
@click.argument("command-prefix")
def generate_command(command_name: str, command_prefix: str):
    allowed_prefixes: list = ["!", ".", "?", "/", ">"]
    if command_prefix not in allowed_prefixes:
        print(
            f"Command prefix provided: {command_prefix} is not supported. Please use one of these: {allowed_prefixes}"
        )
        return
    print("Generating command name: " + command_name)
    generator = GenerateCommand(command_name, command_prefix)
    generator.save_command()


@click.command()
@click.option("--name", default="my-task-name", help="Specify the task name")
@click.argument("task-name")
def generate_task(name, task_name):
    print("Generating command name: " + task_name)
    generator = TaskGeneratorCommand(task_name)
    generator.generate_task_entry(task_name)


commands.add_command(generate_command)
commands.add_command(generate_task)
commands()
