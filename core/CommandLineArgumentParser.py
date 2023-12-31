import json
import re
from from_root import from_root
class CommandLineArgumentParser:
    def __init__(self, commandinput=""):
        self.input = self.process_string(commandinput)

    def calculate_symmetric_difference(self, syntax_to_array, input_to_array):
        symmetric_difference = []

        if syntax_to_array and input_to_array:
            for item in input_to_array:
                if item not in syntax_to_array:
                    symmetric_difference.append(item)
            for item in syntax_to_array:
                if item not in input_to_array:
                    symmetric_difference.append(item)

        return symmetric_difference

    def process_string(self, input_string):
        input_string = input_string.lower()
        pattern = r'\[(.*?)\]'
        matches = re.findall(pattern, input_string)
        if matches:
            for match in matches:
                processed_match = match.replace(" ", "_")
                input_string = input_string.replace(f"[{match}]", processed_match)
        return input_string

    def matchCommand(self, syntax, keyword):
        if re.search(syntax, keyword):
            return True
        else:
            return False

    def commands(self):
        try:
            with open(from_root('config/commands.json')) as f:
               try:
                   commands = json.load(f)
                   return commands['commands'] if 'commands' in commands else None
               except ValueError:
                    return None
        except Exception as e:
            return None

    def generateArgumentAssociationUnique(self, args, keys):
        
        keys = list(keys)
        if len(args) > 1:
            generated = []
            
            if len(keys) < 1:
                current_dict = {}
                for i in range(0, len(args), 2):
                    key = args[i]
                    value = None if i == len(args) - 1 else args[i + 1]

                    if i + 2 < len(args) and args[i + 2] == value:
                        current_dict[key] = None
                    else:
                        if value is not None:
                            current_dict[key] = self.wrap_string_with_underscore(value)
                        else:
                            current_dict[key] = None

                        generated.append(current_dict.copy())
                        current_dict.clear()
                        
                
            else:
                # implement iterating over the arguments
                # if the keys are found 

                for key in keys:
                    
                    if key in args:
                        result_dict = {}
                        index = args.index(key)
                        value = None

                        if self.checkIfIndexIsOutOfRange(args, index + 1):
                            value = args[index + 1] if index + 1 else None

                        result_dict[key] = value

                        if self.checkIfIndexIsOutOfRange(args, index + 1):
                            args.pop(index + 1)
                            
                        args.pop(index)
                        generated.append(result_dict)
                    
                # Add the remaining args at the end
                for i in range(0, len(args), 2):
                    result_dict = {}
                    key = args[i]
                    value = args[i + 1] if i + 1 < len(args) else None
                    result_dict[key] = self.wrap_string_with_underscore(value) if value is not None else None
                    generated.append(result_dict)
                    
                if len(generated) == 1:
                    return generated[0]
                else:
                    return generated
        
        else:
            return None

    def generateArgumentAssociation(self, args):
        if len(args):
            generated = [{}]
            for i in range(len(args) - 1):
                key = args[i]
                if i + 1 < len(args):
                    value = args[i + 1]
                    generated[-1][key] = self.wrap_string_with_underscore(value)
                    generated.append({})
            generated[-1][args[-1]] = None
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
                if arg_details:
                    if 'hasValue' in arg_details and 'required' in arg_details:
                        if arg_details['hasValue'] or arg_details['required']:
                            if ('type' in arg_details and arg_details['type']):
                                arg_list += arg_key + " " + "{" + arg_details['type'] + "} "
                            else:
                                arg_list += arg_key + " " + "{" + arg_key + "}"
        return arg_list

    def find_matching_command(self, input_command="", commands=None):

        input_command = input_command.lower()

        command_matches = []
        # dont remember why i implemented this
        # input_command = self.remove_string_with_hyphen(input_command)
        if (input_command and commands):
            for command_name, command_details in commands.items():
                # dont remember why i implemented this
                #syntax = self.remove_string_with_hyphen(command_details["syntax"])

                syntax = command_details["syntax"].lower()

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

    def validate_arguments(self, command_input=None, arguments=None, command_syntax=None):
        errors = []
        argument_assoc = []
        status = True

        if command_input and arguments:
            input_to_array = command_input.split(" ")
            input_to_array = [element for element in input_to_array if element]


            # Handle required arguments
            # they must all be provided

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

                                    # start checking types
                                    if ('type' in values):
                                        type = values.get('type')
                                        if type is not None:
                                            if type == 'boolean':
                                                if (argument_value not in ['True', 'False', 'true', 'false']):
                                                    status = False
                                                    errors.append(
                                                        f"Argument {argument_key} must be a BOOLEAN. "
                                                        f"Valid values include: [True, False, true, false]")
                                                else:
                                                    argument_assoc.append({argument_key: self.converToBoolean(argument_value)})

                                            elif type == 'array':
                                                if 'accepts' in values and len(values['accepts']):
                                                    if argument_value not in values['accepts']:
                                                        status = False
                                                        errors.append(
                                                            f"Argument {argument_key} must contain one of the values: " + str(
                                                                values['accepts']))
                                                    else:
                                                        argument_assoc.append({argument_key: argument_value})

                                            elif type == 'integer':
                                                convertToInt = self.convertToInteger(argument_value)
                                                if (convertToInt):
                                                    if not self.isInteger(convertToInt):
                                                        status = False
                                                        errors.append(f"Argument {argument_key} must be an INTEGER")
                                                    else:
                                                       argument_assoc.append({argument_key: convertToInt})
                                                else:
                                                    status = False
                                                    errors.append(f"Argument {argument_key} must be an INTEGER.")

                                            elif type == 'float':
                                                convertToFloat = self.converToFloat(argument_value)
                                                if convertToFloat:
                                                    if not self.isFloat(convertToFloat):
                                                        status = False
                                                        errors.append(f"Argument {argument_key} must be a FLOAT")
                                                    else:
                                                        argument_assoc.append({argument_key: convertToFloat})

                                                else:
                                                    status = False
                                                    errors.append(f"Argument {argument_key} must be a FLOAT")
                                            else:
                                                argument_assoc.append({argument_key: self.wrap_string_with_underscore(argument_value)})

                        else:
                            status = False
                            errors.append(f"Argument {argument_key} is REQUIRED and must have a VALUE.")

                    else:
                        status = False
                        errors.append(f"Argument {argument_key} is REQUIRED and must be provided.")

            #handle optional arguments
            #handle them only if they are provided
            #this means checking if they have a value


            syntax_to_array = command_syntax.split(" ")
            difference = self.calculate_symmetric_difference(syntax_to_array, input_to_array)
            last_argument = None



            # this is where i handle
            # the last argument key

            if difference:
                if len(difference) <= 1:
                    last_argument = difference[0]
                else:
                    if len(difference) % 2 == 0:
                        last_argument = difference[-2]
                    else:
                        last_argument = difference[-1]
            else:
                # if the command has some arguments set in
                # it's configuration show an error in case
                # no arguments are provided
                # THIS ERROR IS TRIGGERED only if AT LEAST ONE ARGUMENT
                # has hasValue set to TRUE

                if arguments:
                    hasValuedArguments = False
                    for argument,argument_details in arguments.items():
                        if 'hasValue' in argument_details and argument_details['hasValue'] == True:
                            hasValuedArguments = True


                    if hasValuedArguments:
                        status = False
                        errors.append("No arguments provided.")
                        errors.append("Run: [" + command_input + " help]")


            
            if(last_argument in arguments):
                
                arg_data = arguments[last_argument]

                if('hasValue' in arg_data and arg_data['hasValue'] == True):

                    start_index = input_to_array.index(last_argument)
                    argument_value_index = start_index + 1

                    if (self.checkIfIndexIsOutOfRange(input_to_array, argument_value_index)):

                        if ('hasValue' in arg_data):
                            has_value = arg_data.get('hasValue', False)
                            argument_value = input_to_array[argument_value_index]
                            # Check if the argument value meets the length requirements
                            if has_value and argument_value:


                                # start checking string length
                                if has_value and 'minLength' not in arg_data \
                                        and 'maxLength' not in arg_data \
                                        and argument_value is None and argument_value == " ":
                                    status = False
                                    errors.append(f"Argument {last_argument} MUST have a value.")
                                else:
                                    if ('minLength' in arg_data):
                                        min_length = arg_data.get('minLength')

                                        if min_length is not None and len(argument_value) < min_length:
                                            status = False
                                            errors.append(
                                                f"Argument {last_argument} value is TOO SHORT. Minimum length has to be equal or higher than {min_length}")

                                    if ('maxLength' in arg_data):
                                        max_length = arg_data.get('maxLength')
                                        if max_length is not None and len(argument_value) > max_length:
                                            status = False
                                            errors.append(
                                                f"Argument {last_argument} value is TOO LONG. Maximum length is {max_length}")


                                #start checking type
                                if ('type' in arg_data):
                                    type = arg_data.get('type')
                                    if type is not None:
                                        if type == 'boolean':
                                            if (argument_value not in ['True', 'False', 'true', 'false']):
                                                status = False
                                                errors.append(
                                                    f"Argument {last_argument} must be a BOOLEAN. Valid values include: [True, False, true, false]")

                                        elif type == 'array':

                                            if 'accepts' in arg_data and len(arg_data['accepts']):
                                                if argument_value not in arg_data['accepts']:
                                                    status = False
                                                    errors.append(
                                                        f"Argument {last_argument} is provided and must contain one of the values: " + str(arg_data['accepts']))


                                        elif type == 'integer':
                                            convertToInt = self.convertToInteger(argument_value)
                                            if (convertToInt):
                                                if not self.isInteger(convertToInt):
                                                    status = False
                                                    errors.append(f"Argument {last_argument} must be an INTEGER")

                                            else:
                                                status = False
                                                errors.append(f"Argument {last_argument} must be an INTEGER.")

                                        elif type == 'float':
                                            convertToFloat = self.converToFloat(argument_value)
                                            if convertToFloat:
                                                if not self.isFloat(convertToFloat):
                                                    status = False
                                                    errors.append(f"Argument {last_argument} must be a FLOAT")

                                            else:
                                                status = False
                                                errors.append(f"Argument {last_argument} must be a FLOAT")

                    else:
                        status = False
                        errors.append(f"Argument {last_argument} is provided and must have a VALUE.")

            else:
                argument_assoc = self.generateArgumentAssociation(difference)
                
            if(not argument_assoc and difference):
                argument_assoc = self.generateArgumentAssociationUnique(difference, arguments.keys())

                ## if no argument association can be generated
                ## generate one using the argument
                ## useful for when using the help at the
                ## end of the commands
                
                if argument_assoc is None and last_argument in arguments:
                    #argument_assoc = [{last_argument : last_argument}]
                    argument_assoc = {last_argument : last_argument}
            else:
                input_to_array.pop(0) # remove the command prefix
                argument_assoc = self.generateArgumentAssociationUnique(input_to_array, arguments.keys())
        
        
        return status, errors, argument_assoc

    def validate_command_input(self, command_input, argument=None):
        errors = []
        argument_assoc = []
        status = True

        if command_input and argument:

            input_to_array = command_input.split(" ")
            input_to_array = [element for element in input_to_array if element]

            if(argument in input_to_array):
                start_index = input_to_array.index(argument)
                argument_value_index = start_index + 1


                if (not self.checkIfIndexIsOutOfRange(input_to_array, argument_value_index)):
                    errors.append(f"A value is required at the end of the command.")
                    status = False
                else:
                    arg_value = input_to_array[argument_value_index]
                    if (arg_value is None or arg_value == "" or arg_value == " "):
                        errors.append(f"A value is required at the end of the command.")
                        status = False
                    else:
                        argument_assoc = {argument : arg_value.lower()}

        return status, errors , argument_assoc

    def combine_dictionaries(self, list_of_dicts = None):
        combined_dict = {}
        if list_of_dicts:
            if len(list_of_dicts) >= 2:
                for dictionary in list_of_dicts:
                    combined_dict.update(dictionary)
            else:
                combined_dict = list_of_dicts # no 0 hey kere
        return combined_dict

    def wrap_string_with_underscore(self, text):
        # pattern = r"(\w*_[^_\s]+_\w*)"  # Regular expression pattern to match strings with underscore
        # wrapped_text = re.sub(pattern, r"[\g<0>]", text)
        # return wrapped_text
        return text.lower()

    def seekCommands(self, commands):
        matching_command = self.find_matching_command(self.input, commands)

        if matching_command:
            commandData = commands[matching_command]
            syntax = commandData['syntax']
            desc = commandData['description']
            file = commandData['filePath']
            authorization = commandData['authorization']

            if('hasValue' not in commandData):
                has_value = False
            else:
                has_value = commandData['hasValue']

            if('arguments' not in commandData):
                arguments = {}
            else:
                arguments = commandData['arguments']

            if('slashCommand' not in commandData):
                is_slash = False
            else:
                is_slash = commandData['slashCommand']

            if('middlewares' not in commandData):
                middlewares = []
            else:
                middlewares = commandData['middlewares']

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

            if(not has_value):
                status, errors, args = self.validate_arguments(self.input, arguments, syntax)
            else:
                syntax_to_array = syntax.replace("/","").split(" ")

                if(len(syntax_to_array) > 1):
                    command_arg = syntax_to_array[-1]
                else:
                    command_arg = syntax_to_array[0]

                status, errors, args = self.validate_command_input(self.input, command_arg)
            
         
            
            if (status and not errors):
                return {
                    'status': True,
                    'code': 200,
                    'name': name,
                    'description': desc,
                    'file': file,
                    'authorization': authorization,
                    'syntax': command_syntax,
                    'args': self.combine_dictionaries(args),
                    'hasValue': has_value,
                    'middlewares': middlewares,
                    'slashCommand': is_slash
                }
            else:
                return {
                    'status': status,
                    'code': 200,
                    'name': name,
                    'description': desc,
                    'file': file,
                    'authorization': authorization,
                    'args': None,
                    'syntax': command_syntax,
                    'errors': errors,
                    'hasValue': has_value,
                    'middlewares': middlewares,
                    'slashCommand': is_slash
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
                    arguments = commandData.get('arguments', None)
                    file = commandData.get('filePath')
                    has_value = commandData.get('hasValue', None)
                    is_slash = commandData.get('slashCommand', None)
                    middlewares = commandData.get('middlewares', None)

                    if(not has_value):
                        has_value = False


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
                        'file': file,
                        'hasValue': has_value,
                        'slashCommand': is_slash,
                        'middlewares': middlewares
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
                    if argument_value['type'] not in ['string', 'boolean', 'integer', 'float', 'array']:
                        errors.append("Argument: [" + argument_key + "] key ['type'] must contain one of the "
                                                                     "following values: [string, boolean, integer, "
                                                                     "float, array].")
                        status = False

        return errors, status

    def check_commands_integrity(self, commands=None, data=None):
        errors = []
        status = True

        commands = self.pull_commands_in_the_same_array()

        if commands:
            for command in commands:
                if command['command'] is None or command['command'] == "":
                    errors.append("['syntax'] in " + command["name"] + " was not declared")
                    status = False

                if command['desc'] is None or command['desc'] == "":
                    errors.append("['description'] in " + command["name"] + " was not declared or it is empty")
                    status = False

                if 'authorization' not in command:
                    errors.append("['authorization'] in " + command["name"] + " was not declared.")
                    status = False

                if command['slashCommand'] is None or command['slashCommand'] == "":
                    errors.append("['slashCommand'] in " + command["name"] + " was not declared or it is empty")
                    status = False
                else:
                    if (command['slashCommand'] not in [True, False, "true", "false"]):
                        errors.append("['slashCommand'] in " + command["name"] + " "
                                                                             "has to be set to either 'true' or 'false'")
                        status = False

                if command['file'] is None or command['file'] == "":
                    errors.append("['filePath] in " + command["name"] + " was not declared or it is empty")
                    status = False

                if ('hasValue' not in command or command['hasValue'] is None or command['hasValue'] == ""):
                    errors.append("['hasValue'] in " + command["name"] + " was not declared or it is empty")
                    status = False
                else:
                    if(command['hasValue'] not in [True,False, "true", "false"]):
                        errors.append("['hasValue'] in " + command["name"] + " "
                                                                             "has to be set to either 'true' or 'false'")
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
                    has_value = commandData.get('hasValue', False)
                    is_slash = commandData.get('slashCommand', False)

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
                        'file' : file,
                        'hasValue': has_value,
                        'slashCommand': is_slash
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





