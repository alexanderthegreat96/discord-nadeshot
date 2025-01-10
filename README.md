# Discord Nadeshot v1.6

**Discord Nadeshot** is a high-performance, modular Discord bot framework built from scratch. It offers powerful features for managing commands, events, and tasks with a flexible architecture, ideal for collaborative development and control over every aspect of your bot’s behavior.

## Key Features

- **Object-Oriented Design**: Each command and task is isolated in its own file, promoting clean, modular, and maintainable code.
- **Asynchronous Multi-Threading**: Supports asynchronous tasks that run at scheduled intervals without impacting performance.
- **Event-Driven Architecture**: Built-in support for easy-to-use events, making it simple to extend functionality.
- **Advanced Command Handling**: Includes support for typed arguments and structured command parsing.
- **Middleware Integration**: Middleware support for adding pre/post-execution logic to commands and tasks.
- **Authorization System**: Fine-grained authorization control over who can run specific commands.

## Why Use Discord Nadeshot?

If you're looking for a solution that makes building modular, extensible Discord bots simple, while giving you full control over the architecture and functionality, **Discord Nadeshot** is the framework for you. Say goodbye to constraints imposed by pre-built libraries—this framework gives you complete freedom to design your bot without restrictions.

---

## Getting Started

You can set up **Discord Nadeshot** either by installing it locally or using Docker for a production-like environment. Docker is the recommended option for ease of use and consistent deployment.

### Option 1: Local Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Configure your environment:
    - Modify the `.env` file based on the `.env_sample` template.

### Option 2: Docker Setup (Recommended)

1. Configure your environment:
    - Modify the `.env` file based on the `.env_sample` template.
2. Build and run the project using Docker:
    ```bash
    docker-compose up --build
    ```

---

## Configuration

After setting up, you can further tweak your bot's settings by editing the `config/bot.json` file. Here’s a basic configuration:

```json
{
  "config": {
    "bot-name": "Nadeshot",
    "bot-command-prefix": "/",
    "bot-listens-to": "/nade",
    "bot-description": "Run /nade help for a full list of commands",
    "enable-reset-cooldowns": true,
    "enable-cooldowns": true,
    "cooldown-duration": 15,
    "enable-global-errors": true,
    "enable-automatic-command-helper": false,
    "development-mode": true,
    "enable-multiple-bots": false
  }
}
```
## Command and Task Generation
To speed up development, the framework includes a built-in boilerplate generator for both commands and tasks. This allows you to create new features without starting from scratch.

### Command Generation
To generate a new command:
```bash 
py bin/console.py generate-command my-command-name/sub-command-name
py bin/comsole.py generate-cmmand --command-name my-new-command/some-sub-command --command-prefix ! 
```

If you provide a different command prefix, like ```?``` or ```!```, you have to specify this in ```config/bot.json``` by editing ```bot-command-prefix```.

### Task Generation
To generate a new task:

```bash
py bin/console.py generate-task my-task-name
```
The generated files will be placed in:
  - Commands: `commands` -> `config/commands.json`
  - Tasks: `tasks` -> `config/tasks.json`

## Example Configurations
### Commands Example
This is found ins `config/commands.json`
```json
"commands": {
  "firewall": {
    "commands": {
      "RevokeAll": {
        "syntax": "/firewall revoke-all",
        "description": "Forces the system to revoke all invites across servers.",
        "filePath": "firewall/RevokeAll.py",
        "authorization": ["admin"],
        "hasValue": false,
        "slashCommand": false,
        "middlewares": ["before_force_dm"],
        "arguments": {
          "help": {
            "required": false,
            "hasValue": false
          },
          "list": {
            "required": false,
            "hasValue": false
          },
          "server": {
            "required": false,
            "hasValue": true,
            "minLength": 3,
            "maxLength": 40,
            "type": "integer"
          }
        }
      }
    }
  }
}
```

### Tasks Example
This is found in `config/tasks.json`
```json
"tasks": {
  "LogServerIfNotExist": {
    "file_name": "log_server_if_not_exist.py",
    "class_name": "LogServerIfNotExist",
    "hours": 0,
    "minutes": 30,
    "seconds": 0,
    "enabled": true
  }
}
```
## Middleware

Middlewares in `Discord Nadeshot` act as pre- or post-execution hooks for commands and tasks, similar to middleware in HTTP request handling.
 - Before Middleware: Runs before the command is executed. If it returns false, the command won’t run.
 - After Middleware: Runs after the command is executed, regardless of the result.'
 
Middlewares are defined in the `middlewares` block of the command configuration in `config/commands.json`. Files are prefixed with `before_` or `after_` to clarify when they are run.
```json
"middlewares": ["before_force_dm", "after_log_execution"]
```

---

## Command Arguments

When defining commands, you can specify various types of arguments for fine control over user inputs. Arguments in **Discord Nadeshot** can be configured with properties like required status, type, and constraints such as minimum or maximum length. Below are the common properties you can define for each argument:

### Argument Properties

- **required** (boolean): Specifies whether the argument is mandatory.
- **hasValue** (boolean): Determines if the argument requires a value or can be a flag.
- **minLength** (integer): Sets the minimum length for string arguments.
- **maxLength** (integer): Sets the maximum length for string arguments.
- **type** (string): Defines the type of the argument. Supported types
include:
  - **integer**: A whole number.
  - **string**: A sequence of characters.
  - **float**: A true or false value.
  - **boolean**: Refers to a Discord user (by mention or ID).
  - **array**: Refer to an array

- **accepts** (array): Defines a list of values that can be provided

### Example Configuration

Here’s how you would define arguments for a command in the `commands.json` file:

```json
"commands": {
  "exampleCommand": {
    "syntax": "/example command",
    "description": "A sample command with arguments",
    "filePath": "exampleCommand.py",
    "authorization": ["admin"],
    "hasValue": false,
    "slashCommand": true,
    "middlewares": ["before_validate"],
    "arguments": {
      "user": {
        "required": true,
        "hasValue": true,
        "type": "user"
      },
      "count": {
        "required": false,
        "hasValue": true,
        "type": "integer",
        "minLength": 1,
        "maxLength": 100
      },
      "verbose": {
        "required": false,
        "hasValue": false,
        "type": "boolean"
      },
      "elements": {
        "type": "array",
        "required": true,
        "accepts": [
          "pc",
          "psn",
          "xbox"
        ]
      }
    }
  }
}
```

## Components
There are several other components that can be used to manipulate responses, handle discord object data, interact with the API directly, handle environment variables, interact with redis and so on.

 - ### authorization.admin,root,moderator
   - Contains the code that is getting run each time you add the ```authorization``` directive in your ```config/commands.json```. Additional database logic can be used in here
 - ### utils.cooldown_immune
   - Contains a class which you can tap in if you wish to setup personalized cooldowns for your users
 - ### utils.error_handler
   - Contains a class which gets called during errors. This can be used to actually tap into errors and do something with them
 - ### core.EnvParser
   - This is my custom implementation for reading environment variables. I wanted something that has 0 dependencies and supports a few more features than traditional packages
 - ### core.Api.ApiActions
    - This is a HTTP Request Wrapper that interacts with Didscord's RESTful API. This was implemented as a necessitiy, since the concurrent task mechanism boots up new threads, we cannot hook into the traditional async / await main thread. Therefore, we must run them in sync and not async.
- ### core.Cache
    - A class I built to interact with redis. It's useful for storing data, queueig, dequeueing data
- ### core.Logger
    - This is nothing more than a wrapper around python's std logger, but with color coding and custom structure.
- ### utils.Synced 
    - This is a class that will sync responses to each user avoiding overlapping responses for multiple commands. You should not use self.ctx.response, instead, use Synced.
- ### utils.GuildWrapper
    - Nothing more than a wrapper used for the Guild object. It serves as an elegant way to get data from it.
- ### utils.MemberWrapper
    - A Wrapper for the Member object. Provides getters.
- ### utils.MessageWrapper
    - A wrapper for the Message Object. Provides getters.
- ### utils.UserWrapper
    - A wrapper for the User object. Provides getters.
- ### utils.DiscordUser
    - A wrapper for the User object coming from context. 
- ### utils.DiscordServer
    - A wrapper for the Guild / Server object from context.

### Multi-Bot Handler

Discord’s restrictions on `Intents` for verified apps and other limitations make it challenging to deploy large-scale bots efficiently. To address this, I implemented a multi-bot system that allows multiple bot variants to coexist in servers without overlapping or redundant command handling.

#### Use Case:
- **Homebase Concept**: A primary bot serves as the main handler for commands in a specified server (homebase).
- **Secondary Variants**: Additional bot variants can be invited to servers as needed without all bots responding to the same command simultaneously.

This ensures a clean and efficient command structure while allowing multiple bot instances to exist in the same environment.

---

#### Steps to Set Up:
1. **Obtain Additional Tokens**:
   - Acquire multiple bot tokens to deploy multiple variants.

2. **Deploy Bot Variants**:
   - Deploy each bot instance using its unique token.

3. **Configure Multi-Bot Settings**:
   - Add your configuration to `config/multi-bot.json` (see example below).
   - Enable the `enable_multiple_bots` option in `config/bot.json`.

4. **Environment Setup**:
   - Define each bot's `BOT_VARIANT` in its environment (e.g., `.env` file).
   - Deploy each bot instance into its container or environment.

---

#### Example Configuration for `multi-bot.json`
Heres an example of how to structure your `multi-bot.json` file:

```json
{
    "servers": [
        {
            "server_id": 1167179502175137813,
            "bot-variants": {
                "primary": "BOT_VARIANT_ENV_VALUE_FROM_ENV",
                "others": [
                    "OTHER_BOT_VARIANT_ENV_VALUE_FROM_ENV",
                    "SECOND-VARIANT",
                    "THIRD-VARINT"
                ]
            }
        }
    ]
}

```

**Explanation**:

- **`server_id`**: The unique identifier for the Discord server where this configuration applies. Each Discord server (guild) has a distinct `server_id` that allows bots to recognize and interact with it appropriately.

- **`bot-variants.primary`**: Specifies the bot variant designated as the primary handler for commands in the specified server. This bot will actively process commands, ensuring that only one bot responds to user inputs, preventing command overlap.

- **`bot-variants.others`**: Lists the bot variants present in the server that should not process commands. These bots will remain in the server but will ignore command inputs, allowing for their presence without causing interference or duplicate responses.


### Finale
Please go ahead and explore. There are more things that can be done. If you cannnot do something, just go ahead and open up an issue.