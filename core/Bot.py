from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import discord
import time
import json
import os
from os import path
import importlib
import importlib.util
import sys
import types
from utils.user import user
from core.CommandLineArgumentParser import CommandLineArgumentParser
import traceback

class Bot:
    def __init__(self, ):
        self.config = self.botConfig()
        self.bot = commands.Bot(command_prefix=self.config["bot-command-prefix"],
                                activity=discord.Activity(type=discord.ActivityType.listening,
                                                          name=self.config["bot-listens-to"],
                                                          description=self.config["bot-description"]),
                                intents=discord.Intents.all(), case_insensitive=True)
        self.commands = commands

    def botConfig(self):
        try:
            f = open('config/bot.json', 'r')
            try:
                data = json.load(f)
                return data['config']
            except Exception as e:
                return False
        except Exception as e:
            return False

    def staffList(self):
        try:
            f = open('config/staff.json', 'r')
            try:
                data = json.load(f)
                return data['users']
            except Exception as e:
                return False
        except Exception as e:
            return False

    def staffGroups(self):
        try:
            f = open('config/groups.json', 'r')
            try:
                data = json.load(f)
                return data['groups']
            except Exception as e:
                return False
        except Exception as e:
            return False

    def str_to_class(self, field):
        try:
            identifier = getattr(sys.modules[field], field)
        except AttributeError:
            raise NameError("%s doesn't exist." % field)
        if isinstance(identifier, (types.ClassType, types.TypeType)):
            return identifier
        raise TypeError("%s is not a class." % field)

    def command_list(self):
        try:
            f = open('config/commands.json', 'r')
            try:
                data = json.load(f)
                return data['commands']
            except Exception as e:
                return False
        except Exception as e:
            return False

    def isArray(self, input):
        if (isinstance(input, list)):
            return True
        elif isinstance(input, dict):
            return True
        else:
            return False

    # imports given modules / python files allowing
    # dependency injection

    def path_import(self, absolute_path):
        try:
            spec = importlib.util.spec_from_file_location(absolute_path, absolute_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            return False

    def checkIfItemIsNotEmpty(self, item):
        if (item is not None):
            return True
        elif (item != ''):
            return True
        else:
            return False

    def validateCommandInputs(self, inputs):

        if ('arguments' in inputs and len(inputs['arguments'])):
            for item in inputs['arguments']:
                self.validateCommandInputs(item)
        else:
            pass

    def organize_middlewares(self, middlewares=[]):
        if middlewares:
            before_middlewares = []
            after_middlewares = []
            for middleware in middlewares:
                if middleware.startswith("before_"):
                    before_middlewares.append(middleware)
                elif middleware.startswith("after_"):
                    after_middlewares.append(middleware)

            return {
                "before": before_middlewares,
                "after": after_middlewares
            }
        return []
    def run_middleware(self, ctx, middlewares = []):

        status = True
        error = None
        message = None

        if(middlewares):
            for middleware in middlewares:
                if (path.exists('middlewares/' + middleware + '.py')):
                    commandContents = self.path_import('middlewares/' + middleware + '.py')
                    className = getattr(commandContents, middleware)
                    run = className(ctx)
                    output = run.main()

                    if 'status' in output:
                        if not output['status']:
                            status = False
                            error = output['error']
                        else:
                            status = True
                            if 'message' in output:
                                message = output['message']


        return status, error, message

    def isBanned(self, ctx):
        userInfo = user(ctx)
        status = False

        if (path.exists('authorization/banned.py')):
            commandContents = self.path_import('authorization/banned.py')
            className = getattr(commandContents, 'banned')
            run = className(ctx, userInfo.getUserId)
            output = run.main()
            return output

    def authorize(self, ctx, groups=[]):
        if (groups):
            staffListGroups = self.staffGroups()
            userInfo = user(ctx)
            status = False
            for group in groups:
                if (group in staffListGroups):
                    if (path.exists('authorization/' + group + '.py')):
                        commandContents = self.path_import('authorization/' + group + '.py')
                        className = getattr(commandContents, group)
                        run = className(ctx, userInfo.getUserId())
                        output = run.main()
                        if(output == True):
                            return True

        else:
            status = True
        return status


    def add_commands(self, commandName='dth'):

        print("Injecting: " + commandName)

        @self.bot.before_invoke
        async def resetCooldown(ctx):
            # enable cooldown resets for staff members

            if (self.config['enable-reset-cooldowns']):
                staff = self.staffList()
                userInfo = user(ctx)
                if (str(userInfo.getUserId()) in staff['admin']):
                    return ctx.command.reset_cooldown(ctx)

                if (str(userInfo.getUserId()) in staff['moderator']):
                    return ctx.command.reset_cooldown(ctx)

                if (str(userInfo.getUserId()) in staff['root']):
                    return ctx.command.reset_cooldown(ctx)

        @self.bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandOnCooldown):
                seconds = error.retry_after
                await ctx.send('Hold on, your ability is on cooldown. Re-run the command in: <t:{}:R>'.format(int(time.time() + seconds)),
                               delete_after=seconds)
            # if isinstance(error, commands.CommandNotFound):  # or discord.ext.commands.errors.CommandNotFound as you wrote
            #     await ctx.send("```Unknown command. Run: [/dth help] for a full list of commands.```")
            # raise error

            # if isinstance(error, commands.MissingPermissions):
            #     await ctx.send("``` You do not have permissions to execute this command or this channel does not allow it. ```")
            #     raise error
            #
            if isinstance(error, commands.CommandInvokeError):
                if (self.config['enable-global-errors']):
                    await ctx.send("```Command invoke issues: " + str(error) + "```")
                    raise error
                else:
                    await ctx.send("```There was an issue when running this command.\n"
                                   "You may check for issues like: permissions, channel settings```")

            if (self.config['enable-global-errors']):
                raise error  # re-raise the error so all the errors will still show up in console

        # @

        command_list = self.command_list()

        if(command_list and commandName in command_list):
            if('commands' in command_list[commandName]):
                sub = command_list[commandName]['commands']
            else:
                print ("This command does not have subs " + commandName)

            @commands.cooldown(1, self.config['cooldown-duration'], commands.BucketType.user)
            @self.bot.command(name=commandName, pass_context=True)
            async def item(ctx, *args):
                if('help' in args and self.config['enable-automatic-command-helper']):
                    if(self.config['enable-automatic-command-helper'] == True):
                        parser = CommandLineArgumentParser()
                        helper = parser.build_command_helper()

                        if helper:

                            nadeshotEmbed = discord.Embed(title=self.config['bot-name'],
                                                          description='Command line helper',
                                                          color=discord.Color.blue())
                            nadeshotEmbed.set_footer(text="Powered by Nadeshot BETA")


                            for item in helper:
                                name = item['name']
                                command_str = item['command']
                                desc = item['desc']
                                authorization = item['authorization']
                                arguments = item['arguments']

                                values = desc + "\n" + "```" + command_str + "```\n"
                                nadeshotEmbed.add_field(name=name, value=values, inline=False)


                            await ctx.channel.send(embed=nadeshotEmbed)
                    else:
                        await ctx.channel.send("```Automatic command helper is disabled due to multi-user-type permissions.\n"
                                               "You could use /whatever-command help. That's where helpers are generally stored.```")


                else:
                    providedArguments = self.config['bot-command-prefix'] + "" + commandName + " " + " ".join(args)
                    parser = CommandLineArgumentParser(providedArguments)
                    validation = parser.parse()

                    if (validation['status']):

                        inputArguments = validation['args']

                        authorization = []
                        authorize = True
                        middlewares = self.organize_middlewares(validation['middlewares'])

                        if(len(validation['authorization'])):
                            authorization = validation['authorization']
                            authorize = self.authorize(ctx, authorization)

                        if (not authorize):
                            ctx.channel.send("```This command requires special authorization.```")
                        else:
                            middleware_status = True
                            middleware_error = None
                            middleware_message = None

                            before = []
                            after = []

                            if(middlewares):
                                before = middlewares['before']
                                after = middlewares['after']

                                if before:
                                     middleware_status, middleware_error, middleware_message = self.run_middleware(ctx, before)

                            if middleware_status:
                                if middleware_message:
                                    await ctx.channel.send(middleware_message)
                                try:
                                    commandContents = self.path_import('commands/' + validation['file'])
                                    className = getattr(commandContents, validation['name'])
                                    try:
                                        run = className(self.bot, ctx, args, authorization, inputArguments)
                                        await run.main()
                                    except Exception as e:
                                        if(self.config['development-mode']):
                                            await ctx.channel.send("```Error running class: " + str(e) + "\n"
                                                                   + str(traceback.format_exc()) + "```")
                                        else:
                                            await ctx.channel.send("```System Error. Contact developer```")
                                except Exception as e:
                                    if(self.config['development-mode']):
                                        await ctx.channel.send("```Error importing class: " + str(e) + "\n" + str(traceback.format_exc()) + "```")
                                    else:
                                        await ctx.channel.send("```System Error. Contact developer```")
                            else:
                                await ctx.channel.send("```Error: " + middleware_error + "```")

                            if after:
                                run_after_status, run_after_error, run_after_message = self.run_middleware(ctx, after)
                                if not run_after_status:
                                    await ctx.channel.send("```Error " + run_after_error + "```")
                                else:
                                    if run_after_message:
                                        await ctx.channel.send(run_after_message)


                    else:
                        nadeshotEmbed = discord.Embed(title=self.config['bot-name'],
                                                      description='General information',
                                                      color=discord.Color.blue())
                        nadeshotEmbed.set_footer(text="Powered by Nadeshot BETA")

                        if ("errors" in validation):

                            nadeshotEmbed.add_field(name="Command input", value=validation["name"], inline=False)
                            nadeshotEmbed.add_field(name="Description", value=validation["description"], inline=False)
                            nadeshotEmbed.add_field(name="Example input", value=validation["syntax"], inline=False)

                            errors = ""
                            for error in validation["errors"]:
                                errors += "```" + error + "```"

                            nadeshotEmbed.add_field(name="Errors", value=errors, inline=False)

                        if ("error" in validation):
                            nadeshotEmbed.add_field(name="Error", value=validation['error'], inline=False)

                        await ctx.channel.send(embed=nadeshotEmbed)

    def boot(self):
        print(self.config['bot-name'] + ' started running\nawaiting user input...')
        try:
            self.bot.run(self.config['bot-token'])
        except Exception as e:
            print("Bot token: [" + self.config['bot-token'] + "] is invalid. Please check.")