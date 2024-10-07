# Discord Nadeshot v1.5

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
    "enable-server-age": true,
    "server-age-limit": 60,
    "enable-user-age": true,
    "user-age-limit": 60
  }
}
```
## Command and Task Generation
To speed up development, the framework includes a built-in boilerplate generator for both commands and tasks. This allows you to create new features without starting from scratch.

### Command Generation
To generate a new command:
```bash 
py bin/console.py generate-command my-command-name/sub-command-name
```

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
This is found in `config/taks.json`
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

### Finale
Please go ahead and explore. There are more things that can be done. If you cannnot do something, just go ahead and open up an issue.