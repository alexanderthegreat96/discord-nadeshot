import json
import re

class CommandLineArgumentParser:
    def __init__(self, commandinput=""):
        self.input = commandinput

    def matchCommand(self, syntax, keyword):
        if (re.search(syntax, keyword)):
            return True
        else:
            return False

    def commands(self):
        try:
            with open('config/commands.json') as f:
               try:
                   commands = json.load(f)
                   return commands['commands'] if 'commands' in commands else None
               except ValueError:
                    return None
        except Exception as e:
            return None

    def generateArgumentAssociation(self, args):
        if (len(args)):
            args = list(args)
            generated = {args[i * 2]: args[i * 2 + 1] for i in range(int(len(args) / 2))}
            generated_values = dict.values(generated)
            for item in args:
                if (item not in generated and item not in generated_values):
                    generated[item] = None
            return generated
        else:
            return None

    def isArray(self, input):
        if (isinstance(input, dict)):
            return True
        return False

    def percentage_exact_match(self, arr1, arr2):

        unique_arr1 = [x for x in arr1 if x not in arr2]
        unique_arr2 = [x for x in arr2 if x not in arr1]

        if len(unique_arr1) == 0 and len(unique_arr2) == 0:
            return 100.0  # Both arrays are empty, consider it as 100% match
        elif len(unique_arr1) > 0 or len(unique_arr2) > 0:
            return 0.0  # One of the arrays has unique elements, consider it as 0% match
        else:
            count = 0
            min_length = min(len(arr1), len(arr2))

            for i in range(min_length):
                if arr1[i] == arr2[i]:
                    count += 1
            return (count / min_length) * 100

    def remove_string_with_hyphen(self, string):
        hyphen_index = string.find('-')
        if hyphen_index != -1:
            return string[:hyphen_index]
        else:
            return string

    def command_args_to_string(self, args=None):
        arg_list = ""
        if (args):
            for arg_key, arg_details in args.items():
                if ('type' in arg_details and arg_details['type']):
                    arg_list += arg_key + " " + "{" + arg_details['type'] + "} "
                else:
                    arg_list += arg_key + " " + "{" + arg_key + "}"
        return arg_list

    def find_matching_command(self, input_command="", commands=None):
        command_matches = []
        input_command = self.remove_string_with_hyphen(input_command)
        if (input_command and commands):
            for command_name, command_details in commands.items():
                syntax = self.remove_string_with_hyphen(command_details["syntax"])

                input_syntax = input_command.split(" ")
                syntax_to_list = syntax.split(" ")

                # Remove additional data after the command keyword
                if len(input_syntax) > len(syntax_to_list):
                    input_syntax = input_syntax[:len(syntax_to_list)]

                percentage_match = self.percentage_exact_match(input_syntax, syntax_to_list)
                command_matches.append(
                    {'command': command_name, 'percentage': percentage_match, 'endpoint': command_details['syntax']})

            if command_matches:
                highest_percentage = max(command_matches, key=lambda x: x['percentage'])
                if (highest_percentage['percentage'] > 80.0):
                    highest_percentage_command = highest_percentage['command']
                    return highest_percentage_command

        return None

    def checkIfIndexIsOutOfRange(self, data, index):
        try:
            found = data[index]
            return True
        except IndexError:
            return False

    def isBoolean(self, input):
        return isinstance(input, bool)

    def isInteger(self, input):
        return isinstance(input, int)

    def isFloat(self, input):
        return isinstance(input, float)

    def convertToInteger(self, input):
        try:
            return int(input)
        except ValueError:
            return None

    def converToFloat(self, input):
        try:
            return float(input)
        except ValueError:
            return None

    def converToBoolean(self, input):
        try:
            return bool(input)
        except ValueError:
            return None

    def convert_data_types(self, lst):
        converted_list = []
        for item in lst:
            if isinstance(item, str):
                try:
                    converted_item = int(item)  # Convert string to int
                except ValueError:
                    try:
                        converted_item = float(item)  # Convert string to float
                    except ValueError:
                        converted_item = item  # Leave as string if conversion fails
                converted_list.append(converted_item)
            else:
                converted_list.append(item)
        return converted_list

    def validated_arguments(self, command_input=None, arguments=None):
        errors = []
        argument_assoc = []
        status = True

        if command_input and arguments:
            input_to_array = command_input.split(" ")
            input_to_array = [element for element in input_to_array if element]

            for argument_key, values in arguments.items():

                if ('required' in values and values['required']):
                    if (argument_key in input_to_array):

                        ## If the argument is required and has been provided
                        ## begin the rest of the validation

                        start_index = input_to_array.index(argument_key)
                        argument_value_index = start_index + 1

                        if (self.checkIfIndexIsOutOfRange(input_to_array, argument_value_index)):

                            if ('hasValue' in values):
                                has_value = values.get('hasValue', False)

                                argument_value = input_to_array[argument_value_index]
                                # Check if the argument value meets the length requirements
                                if has_value and argument_value:

                                    if has_value and 'minLength' not in values \
                                            and 'maxLength' not in values \
                                            and argument_value is None and argument_value == " ":
                                        status = False
                                        errors.append(f"Argument {argument_key} MUST have a value.")
                                    else:
                                        if ('minLength' in values):
                                            min_length = values.get('minLength')
                                            if min_length is not None and len(argument_value) < min_length:
                                                status = False
                                                errors.append(f"Argument {argument_key} value is TOO SHORT. Minimum length is {min_length}")
                                        if ('maxLength' in values):
                                            max_length = values.get('maxLength')
                                            if max_length is not None and len(argument_value) > max_length:
                                                status = False
                                                errors.append(f"Argument {argument_key} value is TOO LONG. Maximum length is {max_length}")

                                        if ('type' in values):
                                            type = values.get('type')
                                            if type is not None:

                                                if (type == 'string'):
                                                    if (status):
                                                        argument_assoc.append({argument_key: argument_value})

                                                elif type == 'boolean':
                                                    if(argument_value not in ['True', 'False', 'true', 'false']):
                                                        status = False
                                                        errors.append(f"Argument {argument_key} must be a BOOLEAN. Valid values include: [True, False, true, false]")

                                                    else:
                                                        if (status):
                                                            argument_assoc.append({argument_key: self.converToBoolean(argument_value)})

                                                elif type == 'integer':
                                                    convertToInt = self.convertToInteger(argument_value)
                                                    if(convertToInt):
                                                        if not self.isInteger(convertToInt):
                                                            status = False
                                                            errors.append(f"Argument {argument_key} must be an INTEGER")
                                                        else:
                                                            if (status):
                                                                argument_assoc.append({argument_key: convertToInt})
                                                    else:
                                                        errors.append(f"Argument {argument_key} must be an INTEGER.")

                                                elif type == 'float':
                                                    convertToFloat = self.converToFloat(argument_value)
                                                    if convertToFloat:
                                                        if not self.isFloat(convertToFloat):
                                                            status = False
                                                            errors.append(f"Argument {argument_key} must be a FLOAT")
                                                        else:
                                                            if (status):
                                                                argument_assoc.append({argument_key: convertToFloat})
                                                    else:
                                                        errors.append(f"Argument {argument_key} must be a FLOAT")

                        else:
                            status = False
                            errors.append(f"Argument {argument_key} is REQUIRED and must have a VALUE.")

                    else:
                        status = False
                        errors.append(f"Argument {argument_key} is REQUIRED and must be provided.")

        return status, errors, argument_assoc

    def seekCommands(self, commands):
        matching_command = self.find_matching_command(self.input, commands)

        if matching_command:
            commandData = commands[matching_command]
            syntax = commandData['syntax']
            desc = commandData['description']
            file = commandData['filePath']
            authorization = commandData['authorization']
            arguments = commandData['arguments']

            path_explode = file.split("/")
            name = path_explode[-1]
            name = name.replace(".py","")

            syntax_args = None
            if arguments:
                syntax_args = self.command_args_to_string(arguments)

            command_syntax = ""
            if syntax:
                if syntax_args:
                    command_syntax = syntax + " " + syntax_args
                else:
                    command_syntax = syntax

            status, errors, args = self.validated_arguments(self.input, arguments)

            if (status and not errors):
                return {
                    'status': True,
                    'code': 200,
                    'name': name,
                    'description': desc,
                    'file': file,
                    'authorization': authorization,
                    'syntax': command_syntax,
                    'args': args
                }
            else:
                return {
                    'status': status,
                    'code': 200,
                    'name': name,
                    'description': desc,
                    'syntax': command_syntax,
                    'errors': errors
                }

        else:
            return {'status': False, 'error': 'Command not found. Please check the command line helper.', 'code': 404}

    def pull_commands_in_the_same_array(self, commands=None, data=None):
        if not commands:
            commands = self.commands()

        if not data:
            data = []

        if commands:
            for command in commands:
                if "commands" in commands[command] and commands[command]["commands"]:
                    nested_data = self.pull_commands_in_the_same_array(commands[command]["commands"])
                    data.extend(nested_data)
                else:
                    commandData = commands[command]
                    name = self.camelcase_to_uppercase(command)
                    syntax = commandData.get('syntax', None)
                    desc = commandData.get('description', None)
                    authorization = commandData.get('authorization')
                    arguments = commandData.get('arguments')
                    file = commandData.get('filePath')

                    syntax_args = None
                    if arguments:
                        syntax_args = self.command_args_to_string(arguments)

                    command_syntax = ""
                    if syntax:
                        if syntax_args:
                            command_syntax = syntax + " " + syntax_args
                        else:
                            command_syntax = syntax

                    data.append({
                        'name': name,
                        'command': command_syntax,
                        'desc': desc,
                        'authorization': authorization,
                        'arguments': arguments,
                        'file': file
                    })

        return data

    def check_args_integrity(self, arguments=None):
        status = True
        errors = []
        if arguments:
            for argument_key, argument_value in arguments.items():
                if 'required' not in argument_value:
                    errors.append("Argument: [" + argument_key + "] is missing ['required'] key.")
                    status = False
                else:
                    if argument_value['required'] not in ['true', 'false', True, False]:
                        errors.append("Argument: [" + argument_key + "] key: ['required'] must be a boolean.")
                        status = False

                if ('hasValue' not in argument_value):
                    errors.append("Argument: [" + argument_key + "] is missing ['hasValue'] key.")
                    status = False
                else:
                    if argument_value['hasValue'] not in ['true', 'false', True, False]:
                        errors.append("Argument: [" + argument_key + "] key: ['hasValue'] must be a boolean.")
                        status = False

                if 'minLength' in argument_value:
                    if not self.isInteger(argument_value['minLength']):
                        errors.append("Argument: [" + argument_key + "] key: ['minLength'] must be an integer.")
                        status = False

                if 'maxLength' in argument_value:
                    if not self.isInteger(argument_value['maxLength']):
                        errors.append("Argument: [" + argument_key + "] key: ['maxLength'] must be an integer.")
                        status = False

                if 'type' in argument_value:
                    if argument_value['type'] not in ['string', 'boolean', 'integer', 'float']:
                        errors.append("Argument: [" + argument_key + "] key ['type'] must contain one of the "
                                                                     "following values: [string, boolean, integer, "
                                                                     "float].")
                        status = False

        return errors, status

    def check_commands_integrity(self, commands=None, data=None):
        errors = []
        status = True

        commands = self.pull_commands_in_the_same_array()

        if commands:
            for command in commands:
                if command['command'] is None or command['command'] == "":
                    errors.append("['syntax'] was not declared")
                    status = False

                if command['desc'] is None or command['desc'] == "":
                    errors.append("['description'] was not declared or it is empty")
                    status = False

                if command['file'] is None or command['file'] == "":
                    errors.append("['filePath] was not declared or it is empty")
                    status = False

                if command['arguments'] is not None:
                    arg_errors, arg_status = self.check_args_integrity(command['arguments'])
                    if not arg_status:
                        errors.extend(arg_errors)
                        status = False

        return errors, status

    def camelcase_to_uppercase(self,camelcase_string):
        words = re.findall(r'[A-Z]?[a-z]*', camelcase_string)
        capitalized_words = [word.capitalize() if word else word.lower() for word in words]
        return ' '.join(capitalized_words)
    def build_command_helper(self, commands=None, data=None):
        if not commands:
            commands = self.commands()

        if not data:
            data = []

        if commands:
            for command in commands:
                if "commands" in commands[command] and commands[command]["commands"]:
                    nested_data = self.build_command_helper(commands[command]["commands"])
                    data.extend(nested_data)
                else:
                    commandData = commands[command]
                    name = self.camelcase_to_uppercase(command)
                    syntax = commandData.get('syntax', None)
                    desc = commandData.get('description', None)
                    authorization = commandData.get('authorization')
                    arguments = commandData.get('arguments')
                    file = commandData.get('filePath')

                    syntax_args = None
                    if arguments:
                        syntax_args = self.command_args_to_string(arguments)

                    command_syntax = ""
                    if syntax:
                        if syntax_args:
                            command_syntax = syntax + " " + syntax_args
                        else:
                            command_syntax = syntax

                    data.append({
                        'name': name,
                        'command': command_syntax,
                        'desc': desc,
                        'authorization': authorization,
                        'arguments': arguments,
                        'file' : file
                    })

        return data
    ## Process the input and handle everything else
    def parse(self):
        check_errors, check_status = self.check_commands_integrity()
        if(check_status):
            commands = self.commands()
            results = []

            if commands:
                for command in commands:
                    if("commands" in commands[command] and commands[command]["commands"]):
                        results.append(self.seekCommands(commands[command]['commands']))
                    else:
                        results.append(self.seekCommands({command: commands[command]}))

                if results:
                    found = None
                    for result in results:
                        if('code' in result and result['code'] == 200):
                            found = result
                    if found is not None:
                        return found
                    else:
                        return {'status': False, 'error': 'No command found. Check the command line helper.'}
                else:
                    return {'status': False, 'error': 'No command found for your input. Check the command line helper.'}
            else:
                return {'status': False, 'error': "No commands found"}
        else:
            return {'status': False, 'error': " \n". join(check_errors)}





