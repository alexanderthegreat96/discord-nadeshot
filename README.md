
# discord-nadeshot-beta

## 
````
 __     __   __   __   __   __                __   ___  __        __  ___     __   ___ ___         
|  \ | /__` /  ` /  \ |__) |  \ __ |\ |  /\  |  \ |__  /__` |__| /  \  |  __ |__) |__   |   /\     
|__/ | .__/ \__, \__/ |  \ |__/    | \| /~~\ |__/ |___ .__/ |  | \__/  |     |__) |___  |  /~~\

````
Rewrite of the previous framework: dth-discord-py


## Installation

Setup is very simple and staight forward.

```bash
  1. Clone the repository
  2. Run pip install -r requirements.txt
  3. cd into your folder
  4. Generate your commands and customize additonal options
  5. Define your bot configuration within config/bot.json
  6. Define your groups within groups.json
  7. Manage authentication middlewares inside authorization folder
  8. Boot your bot using python3 main.py
```

## Usage:

```bash
Run: 
 - py bin/console.py generate myCommand
 - py bin/console.py generate myCommand/subcomand

This will automatically generate the command files and append the command configuration

You may alter the configuration further by appending additional argument requirements, such as the ones in the example bellow
```
### Commands Configuration Sample
```json

{
  "commands": {
    "dth": {
      "commands": {
        "pcTrack": {
          "syntax": "/dth pc track",
          "description": "Awaiting developer description",
          "filePath": "dth/pc/Track.py",
          "authorization": [],
          "arguments": {
            "-u": {
              "required": true,
              "hasValue": true
            }
          }
        },
        "psnTrack": {
          "syntax": "/dth psn track",
          "description": "Awaiting developer description",
          "filePath": "dth/psn/Track.py",
          "authorization": [],
          "arguments": {}
        },
        "xblTrack": {
          "syntax": "/dth xbl track",
          "description": "Awaiting developer description",
          "filePath": "dth/xbl/Track.py",
          "authorization": [],
          "arguments": {}
        }
      }
    },
    "NewCommand": {
      "syntax": "/NewCommand",
      "description": "Awaiting developer description",
      "filePath": "NewCommand.py",
      "authorization": [],
      "arguments": {}
    }
  }
}
```
### Command File Sample

```python

import discord
import asyncio

class Track:
    def __init__(self, bot, ctx, args, authorization, inputArguments):
        self.bot = bot
        self.ctx = ctx
        self.authorization = authorization
        self.args = args
        self.inputArguments = inputArguments


    async def main(self):
        await self.ctx.channel.send("```This is the Track command output within commands folder.```")
```
All the code is ran within the main function, define additional functions and invoke them within main if needed.

### Why use this framework?
Simply because it makes your code clean, organized, does additional checks for you.

### Features:
 - Automatic Command Discovery
 - Authorization Middlewares which can be customized
 - Built in access to all discord options for generating embeds, outputting data and more
 - Easy to use CLI that generates most of the boilerplate code and configurations
 - Built to last