from os import path
import re
import os
import json
from from_root import from_root

def generate_command_name(command=None):
    if(len(command) > 1):
        command.pop(0)
        command_string = " ".join(command)
        return convert_string_to_camelcase(command_string)
    else:
        return convert_string_to_camelcase(command)

def generate_file_path(command=None,filename=None):
    if(len(command) > 1):
        command.pop(-1)
        return "/".join(command) + "/" + filename + ".py"
    else:
        return command + "/" + filename + ".py"
def convert_string_to_camelcase(string):
    words = string.split()
    camelcase_words = [words[0].lower()] + [word.title() for word in words[1:]]
    return ''.join(camelcase_words)

def camelcase_to_uppercase(camelcase_string):
    words = re.findall(r'[A-Z]?[a-z]*', camelcase_string)
    capitalized_words = [word.capitalize() if word else word.lower() for word in words]
    return ''.join(capitalized_words)
def make_command_array(command_camel_case=None, command_string=None, command_file_path=None):
    if(command_camel_case and command_string and command_file_path):
        return {
            command_camel_case : {
                "syntax": command_string,
                "description": "Awaiting developer description",
                "filePath": command_file_path,
                "authorization": [],
                "arguments": {}
            }
        }
    return None
def generate_class_name(command_data=None):
    if(len(command_data) > 1):
        return command_data[-1].capitalize()
    else:
        return "".join(command)
def appendCommandInConfig(command='command'):

    # generate commands.json in case it doesn't exist

    if(not path.exists(from_root('config/commands.json'))):
        with open(from_root('config/commands.json'), 'w') as f:
            json.dump({'commands' : {}}, f, indent=2)


    try:
        # try opening it up
        f = open(from_root('config/commands.json'), 'r')
        try:
            data = json.load(f)

            if("/" in command):

                py_file_path = command
                command_parts = py_file_path.split("/")
                root_command = command_parts[0]

                command_class_name = generate_class_name(command_parts)
                command_name = generate_command_name(command_parts)
                command_string = "/" + root_command + " " + " ".join(command_parts)
                file_path = root_command + "/" + generate_file_path(command_parts, command_class_name)
                command_array = make_command_array(command_name,command_string,file_path)


                if root_command in data["commands"]:
                    data["commands"][root_command]["commands"].update(command_array)
                    try:
                        with open(from_root('config/commands.json'), 'w') as f:
                            try:
                                json.dump(data, f, indent=2)
                                return "JSON Structure for command file:" + file_path + " appended to commands.json"
                            except Exception as e:
                                return "There as an error dumping json structure for " + file_path + ". Error: " + str(e)
                    except Exception as e:
                        return "There was an error opening config/commands.json. Error: " + str(e)
                else:
                    data["commands"][root_command]={}
                    data["commands"][root_command]["commands"] = {}
                    data["commands"][root_command]["commands"].update(command_array)

                    try:
                        with open(from_root('config/commands.json'), 'w') as f:
                            try:
                                json.dump(data, f, indent=2)
                                return "JSON Structure for command file:" + file_path + " appended to commands.json"
                            except Exception as e:
                                return "There as an error dumping json structure for " + file_path + ". Error: " + str(e)
                    except Exception as e:
                        return "There was an error opening config/commands.json. Error: " + str(e)
            else:
                command_string = command
                file_path = command + ".py"

                command_array = {
                    command: {
                        "syntax": "/" + command_string,
                        "description": "Awaiting developer description",
                        "filePath": file_path,
                        "authorization": [],
                        "arguments": {}
                    }
                }

                if(command not in data["commands"]):
                    data["commands"].update(command_array)

                    try:
                        with open(from_root('config/commands.json'), 'w') as f:
                            try:
                                json.dump(data, f, indent=2)
                                return "JSON Structure for command file:" + file_path + " appended to commands.json"
                            except Exception as e:
                                return "There as an error dumping json structure for " + file_path + ". Error: " + str(
                                    e)
                    except Exception as e:
                        return "There was an error opening config/commands.json. Error: " + str(e)



        except Exception as e:
            return "Error trying to handle the commands.json file: " + str(e)
    except Exception as e:
        return "Error trying to open the commands.json file: " + str(e)


def generateCommand(command=''):
    if ('/' in command):
        filePath = os.path.basename(command)
        dirPath = os.path.dirname(command)

        if(not path.exists('commands/' + dirPath + '/' + filePath.capitalize() + '.py')):

            if not os.path.exists('commands/'+ dirPath):
                os.makedirs('commands/' + dirPath)
            else:
                pass


            content = r"""import discord
import asyncio

class """+filePath.capitalize()+""":
    def __init__(self, bot, ctx, args, authorization, inputArguments):
        self.bot = bot
        self.ctx = ctx
        self.authorization = authorization
        self.args = args
        self.inputArguments = inputArguments


    async def main(self):
        await self.ctx.channel.send("```This is the """+filePath.capitalize()+""" command output within commands folder.```")
    """

            openFile = open('commands/' + dirPath + '/' + filePath.capitalize() + '.py', "w")
            openFile.write(content)
            openFile.close()

        return "Command file " + filePath.capitalize() + ".py created in commands/" + dirPath
    else:

        if (path.exists('commands/' + command + '.py')):
            return 'Could not generate command file. The file [commands/'+command+'.py] already exists. Remove it and try again.'
        fileContents = r"""import discord
import asyncio

class """ + camelcase_to_uppercase(command) + """:
    def __init__(self, bot, ctx, args, authorization, inputArguments):
        self.bot = bot
        self.ctx = ctx
        self.authorization = authorization
        self.args = args
        self.inputArguments = inputArguments


    async def main(self):
        await self.ctx.channel.send("```This is the """ + camelcase_to_uppercase(command) + """ command output within commands folder.```")
    """

        f = open('commands/' +camelcase_to_uppercase(command)+ '.py', "w")
        f.write(fileContents)
        f.close()

        return "Command file " + command + ".py created in commands/"