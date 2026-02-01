# Discord Nadeshot v2.1.0

**Discord Nadeshot** is a high-performance, modular Discord bot framework built from scratch. It offers powerful features for managing commands, events, and tasks with a flexible architecture, ideal for collaborative development and complete control over every aspect of your bot's behavior.

## Key Features

- **Object-Oriented Design**: Each command and task is isolated in its own file, promoting clean, modular, and maintainable code
- **Asynchronous Multi-Threading**: Supports asynchronous tasks that run at scheduled intervals without impacting performance
- **Event-Driven Architecture**: Built-in support for easy-to-use events, making it simple to extend functionality
- **Advanced Command Handling**: Includes support for typed arguments and structured command parsing
- **Middleware Integration**: Middleware support for adding pre/post-execution logic to commands and tasks
- **Authorization System**: Fine-grained authorization control over who can run specific commands
- **Programmatic Control**: No slash-commands by default—everything is handled programmatically, giving you full control
- **Multi-Bot Support**: Deploy multiple bot variants in the same environment without conflicts
- **Task Scheduling**: Built-in task scheduling system with configurable intervals
- **CLI Generators**: Built-in tools for scaffolding commands, tasks, and middlewares
- **Comprehensive Testing**: 230+ unit tests with excellent coverage

## Why Use Discord Nadeshot?

If you're looking for a solution that makes building modular, extensible Discord bots simple while giving you full control over the architecture and functionality, **Discord Nadeshot** is the framework for you. Say goodbye to constraints imposed by pre-built libraries—this framework gives you complete freedom to design your bot without restrictions.

---

## Getting Started

### Prerequisites

- Python 3.12+
- pip or conda
- Docker & Docker Compose (optional but recommended)
- A Discord Bot Token

### Quick Start: Local Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd discord-nadeshot
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure your environment:
   ```bash
   cp .env_sample .env
   # Edit .env and add your Discord bot token and other settings
   ```

4. Run the bot:
   ```bash
   python main.py
   ```

For Docker deployment, see the [Docker Deployment](#docker-deployment) section below.

---

## Configuration

After setup, configure your bot by editing `config/bot.json`:

```json
{
  "config": {
    "bot-name": "Nadeshot",
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

### Configuration Keys Explained

| Key | Description | Example |
|-----|-------------|---------|
| **bot-name** | The name of the bot as it appears to users | `"Nadeshot"` |
| **bot-listens-to** | Primary command/keyword the bot listens for | `"/nade"` |
| **bot-description** | Helper message for users | `"Run /nade help for commands"` |
| **enable-reset-cooldowns** | Allow resetting command cooldowns | `true` |
| **enable-cooldowns** | Enable cooldowns to prevent spamming | `true` |
| **cooldown-duration** | Cooldown duration in seconds | `15` |
| **enable-global-errors** | Global error handling and notifications | `true` |
| **enable-automatic-command-helper** | Auto-generate help messages | `false` |
| **development-mode** | Enable development mode for debugging | `true` |
| **enable-multiple-bots** | Allow multiple bot instances | `false` |

---

## Makefile Guide

The project includes a comprehensive `Makefile` that simplifies common development tasks.

### Virtual Environment Management

**Setup virtual environment:**
```bash
make venv-create
```
Creates a Python virtual environment and installs all dependencies.

**Clean virtual environment:**
```bash
make venv-clean
```
Removes and reinstalls the virtual environment.

### Testing

**Run all tests:**
```bash
make test
```
Executes the complete test suite (230+ tests).

**Run tests with coverage:**
```bash
make test-cov
```
Runs tests and generates a detailed coverage report.

**Run unit tests only:**
```bash
make test-unit
```
Executes unit tests excluding integration tests.

**Run tests in watch mode:**
```bash
make test-watch
```
Continuously monitors test files and reruns tests on changes.

### Docker - Development

**Build development image:**
```bash
make dev-build
```
Builds the development Docker image with file watching.

**Start development environment:**
```bash
make dev-up
```
Starts the bot in development mode with auto-reload.

**Stop development environment:**
```bash
make dev-down
```
Stops the development container.

### Docker - Production

**Build production image:**
```bash
make prod-build
```
Builds the optimized production Docker image.

**Start production environment:**
```bash
make prod-up
```
Starts the bot in production mode.

**Stop production environment:**
```bash
make prod-down
```
Stops the production container.

### Other Commands

**View all available targets:**
```bash
make help
```
Displays all available make commands.

**Clean build artifacts:**
```bash
make clean
```
Removes Docker images, containers, and temporary files.

---

## Docker Deployment

### Development Setup

The development Docker setup includes automatic file watching, so code changes are immediately reflected without restarting.

**Step 1: Configure Environment**
```bash
cp .env_sample .env
# Edit .env with your Discord bot token
```

**Step 2: Build and Start**
```bash
make dev-build
make dev-up
```

**Step 3: View Logs**
```bash
docker-compose -f docker-compose.dev.yml logs -f
```

**Step 4: Stop the Bot**
```bash
make dev-down
```

**Benefits:**
- Automatic code reload on file changes
- Full source code mounted as volumes
- Perfect for rapid development and testing
- Identical to production environment

### Production Setup

The production Docker setup is optimized for performance without file watching overhead.

**Step 1: Configure Environment**
```bash
cp .env_sample .env
# Edit .env with production settings
```

**Step 2: Build and Start**
```bash
make prod-build
make prod-up
```

**Step 3: View Logs**
```bash
docker-compose -f docker-compose.prod.yml logs -f
```

**Step 4: Manage the Bot**

View running containers:
```bash
docker-compose -f docker-compose.prod.yml ps
```

Restart the bot:
```bash
docker-compose -f docker-compose.prod.yml restart
```

Stop the bot:
```bash
make prod-down
```

**Benefits:**
- Optimized image size
- No file watching overhead
- Better performance
- Production-ready

### Docker Compose Files

- **docker-compose.dev.yml**: Development configuration
  - Uses `Dockerfile.dev` with `watcher-docker` tool
  - Mounts source code as volumes for live reloading
  - Best for rapid development

- **docker-compose.prod.yml**: Production configuration
  - Uses `Dockerfile.prod` for lean image
  - No file watching
  - Recommended for deployed bots

### Environment Variables

Set these in your `.env` file:

```bash
# Discord Bot Configuration
DISCORD_TOKEN=your_bot_token_here
BOT_VARIANT=primary  # For multi-bot setups

# Redis Configuration (if using Cache)
REDIS_HOST=redis
REDIS_PORT=6379

# Other Settings
DEVELOPMENT_MODE=true  # Set to false in production
```

---

## CLI Tools & Code Generation

The framework includes built-in CLI tools for scaffolding commands, tasks, and middlewares, saving you time during development.

### Command Generation

Generate a new command:
```bash
python bin/console.py generate-command my-command-name
python bin/console.py generate-command admin/ban-user --prefix !
```

**Options:**
- `--name`: Command name (supports nested paths with `/`)
- `--prefix`: Command prefix (default: `/`, also: `!`, `.`, `?`, `>`)

### Task Generation

Generate a new scheduled task:
```bash
python bin/console.py generate-task my-task-name
python bin/console.py generate-task daily-cleanup
```

### Middleware Generation

Generate before/after middleware:
```bash
python bin/console.py generate-middleware rate-limiter before
python bin/console.py generate-middleware audit-log after
```

### Generated Files

- **Commands**: Python files go to `commands/`, config entries to `config/commands.json`
- **Tasks**: Python files go to `tasks/`, config entries to `config/tasks.json`
- **Middlewares**: Python files go to `middlewares/`, prefixed with `before_` or `after_`

---

## Configuration Examples

### Command Configuration

This is found in `config/commands.json`:

```json
{
  "commands": {
    "firewall": {
      "authorization": ["admin"],
      "middlewares": ["before_permission_check"],
      "commands": {
        "RevokeAll": {
          "syntax": "/firewall revoke-all",
          "description": "Revokes all invites across servers",
          "filePath": "firewall/RevokeAll.py",
          "authorization": ["admin"],
          "hasValue": false,
          "slashCommand": false,
          "middlewares": ["before_force_dm"],
          "arguments": {
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
}
```

### Task Configuration

This is found in `config/tasks.json`:

```json
{
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
}
```

---

## Middleware System

Middlewares act as pre- or post-execution hooks for commands, similar to HTTP middleware patterns.

### Middleware Types

- **Before Middleware**: Runs before command execution. Return `false` to cancel the command
- **After Middleware**: Runs after command execution, regardless of result

### Configuring Middlewares

Define middlewares in command configuration:

```json
"middlewares": ["before_permission_check", "after_log_execution"]
```

### Creating Middlewares

Use the CLI generator:

```bash
python bin/console.py generate-middleware rate-limiter before
python bin/console.py generate-middleware audit-log after
```

Generated files are placed in `middlewares/` with appropriate prefixes.

---

## Command Arguments

Define arguments to control user input for commands.

### Argument Properties

- **required** (boolean): Whether argument is mandatory
- **hasValue** (boolean): Whether argument requires a value
- **minLength** (integer): Minimum string length
- **maxLength** (integer): Maximum string length
- **type** (string): Argument type (`integer`, `string`, `float`, `boolean`, `user`, `array`)
- **accepts** (array): List of acceptable values

### Example Configuration

```json
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
  "platform": {
    "type": "array",
    "required": true,
    "accepts": ["pc", "psn", "xbox"]
  }
}
```

---

## Core Components & Architecture

### Authorization System

**Location**: `authorization/` directory

Implements role-based access control:

- **Admin** (`admin.py`): Administrative privileges
- **Moderator** (`moderator.py`): Moderation capabilities
- **Root** (`root.py`): Full system access

Add authorization via `authorization` directive in `config/commands.json`.

### Utility Components

| Component | Purpose |
|-----------|---------|
| **CooldownImmune** | Personalized cooldown management for users |
| **SyncedResponse** | Synchronize responses, avoid message overlaps |
| **GuildWrapper** | Wrapper for Discord Guild/Server objects |
| **MemberWrapper** | Wrapper for Discord Member objects |
| **MessageWrapper** | Wrapper for Discord Message objects |
| **UserWrapper** | Wrapper for Discord User objects |
| **DiscordUser** | Extract user info from command context |
| **DiscordServer** | Extract server info from command context |

### Core Services

| Service | Purpose |
|---------|---------|
| **Logger** | Color-coded logging with custom structure |
| **Config** | Configuration loading and management |
| **EnvParser** | Zero-dependency environment variable parser |
| **Cache** | Redis wrapper for data storage and queuing |
| **DiscordApi** | HTTP client for Discord's REST API |
| **CommandLogger** | Specialized command execution logger |

### Event System

The `events/` directory contains handlers for Discord lifecycle events:

- `on_message.py`: Message creation
- `on_message_edit.py`: Message editing
- `on_message_delete.py`: Message deletion
- `on_member_join.py`: Member joins
- `on_member_remove.py`: Member leaves
- `on_member_ban.py`: Member bans
- `on_member_unban.py`: Member unbans
- `on_guild_join.py`: Bot joins server

### Factory Pattern

**EmbedFactory** (`factory/EmbedFactory.py`)
- Creates Discord embeds with consistent styling
- Supports color mapping and custom formatting

**MessageFactory** (`factory/MessageFactory.py`)
- Generates formatted messages
- Handles direct and regular messages

---

## Multi-Bot Handler

Deploy multiple bot variants in the same environment without conflicts.

### Use Case

- **Primary Bot**: Main handler for commands in specified servers
- **Secondary Variants**: Additional bots that don't process commands

### Setup Steps

1. **Obtain Multiple Bot Tokens**: Create separate Discord bot applications

2. **Deploy Variants**: Deploy each with its unique token

3. **Configure Multi-Bot Settings**: Edit `config/multi-bot.json`

4. **Set Environment Variables**: Define `BOT_VARIANT` for each instance

### Example `multi-bot.json`

```json
{
    "servers": [
        {
            "server_id": 1167179502175137813,
            "bot-variants": {
                "primary": "PRIMARY_BOT",
                "others": ["SECONDARY_BOT", "TERTIARY_BOT"]
            }
        }
    ]
}
```

| Property | Description |
|----------|-------------|
| **server_id** | Unique Discord server identifier |
| **primary** | Bot variant that processes commands |
| **others** | Bot variants that ignore commands |

---

## Project Structure

```plaintext
discord-nadeshot/
├── authorization/          # Role-based access control
├── bin/                    # CLI tools and generators
│   └── commands/           # Command/task/middleware generators
├── commands/               # Command implementations
├── config/                 # Configuration JSON files
├── core/                   # Core framework components
├── events/                 # Discord event handlers
├── factory/                # Factory pattern implementations
├── middlewares/            # Before/after middleware
├── services/               # External API integrations
├── tasks/                  # Scheduled background tasks
├── tests/                  # Test suite (230+ tests)
├── utils/                  # Utility and wrapper classes
├── .env_sample             # Environment variable template
├── .gitignore
├── Dockerfile.dev          # Development Docker image
├── Dockerfile.prod         # Production Docker image
├── docker-compose.dev.yml  # Development orchestration
├── docker-compose.prod.yml # Production orchestration
├── Makefile                # Build and test automation
├── README.md
├── main.py                 # Bot entry point
├── requirements.txt        # Python dependencies
└── watcher-*               # File watchers for development
```

| Directory | Purpose |
|-----------|---------|
| **authorization/** | Role-based access control |
| **bin/** | CLI tools for code generation |
| **commands/** | Discord command implementations |
| **config/** | JSON configuration files |
| **core/** | Core framework components |
| **events/** | Discord event listeners |
| **factory/** | Object creation factories |
| **middlewares/** | Pre/post-execution hooks |
| **services/** | External service integrations |
| **tasks/** | Scheduled background tasks |
| **tests/** | Comprehensive test suite |
| **utils/** | Helper classes and wrappers |

---

## Testing

The project includes a comprehensive test suite with 230+ tests covering all major components.

### Running Tests

**All tests:**
```bash
make test
```

**With coverage report:**
```bash
make test-cov
```

**Watch mode (rerun on changes):**
```bash
make test-watch
```

**Unit tests only:**
```bash
make test-unit
```

### Test Coverage Highlights

- **MiddlewareGenerator**: 100% coverage
- **TaskGenerator**: 98% coverage
- **CommandGenerator**: 89% coverage
- **Config, CooldownImmune, MessageFactory**: 100% coverage
- **SyncedResponse**: 93% coverage

Run `make test-cov` for a complete breakdown of all modules.

---

## Troubleshooting

### Common Issues

**Bot doesn't respond to commands:**
- Verify `DISCORD_TOKEN` in `.env`
- Check bot permissions in Discord server
- Ensure command prefix matches `bot-listens-to` in `config/bot.json`

**Docker container won't start:**
- Check logs: `docker-compose logs -f`
- Verify `.env` file exists with valid token
- Ensure port 8000 is available (or update docker-compose)

**Tests failing:**
- Run `make venv-clean` then `make venv-create`
- Ensure Python 3.12+ is installed
- Check `requirements.txt` is up to date

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

---

## Support & Resources

- **Documentation**: Review examples in this README
- **Code Examples**: Check the test suite for usage patterns
- **Issues**: Open a GitHub issue for bugs or feature requests
- **Discussion**: Use GitHub discussions for questions

---

## License

MIT License - See LICENSE.md for details

Copyright (c) 2025 alexanderthegreat96

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software") to use, modify, and distribute subject to the terms and conditions of the MIT License.

---

## Changelog

### v2.0.9
- Added comprehensive test suite (230+ tests)
- Implemented Makefile for common development tasks
- Separated Docker configurations for development and production
- Improved documentation and examples
- Enhanced CLI generators for commands, tasks, and middlewares

---

**Happy building! 🚀**
