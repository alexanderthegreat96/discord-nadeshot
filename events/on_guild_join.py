import datetime
from utils.config import Config


class OnGuildJoin:
    def __int__(self, guild, bot):
        self.guild = guild
        self.bot = bot

    async def main(self):
        config = Config.bot_config
        if config:
            if 'enable-server-age' in config and config['enable-server-age'] \
                    and 'server-age-limit' in config and config['server-age-limit']:

                today = datetime.datetime.now().date()
                server_creation_date = self.guild.created_at.date()
                days_old = (today - server_creation_date).days

                server_id = self.guild.id
                server_name = self.guild.name
                owner_id = self.guild.owner.id

                if days_old >= config['server-age-limit']:
                    if not check['status']:

                        try:
                            server_info = await self.bot.fetch_guild(server_id)
                            for channel in guild.text_channels:
                                if channel.permissions_for(guild.me).send_messages:
                                    await channel.send(
                                        "```There was an error joining this bot: " + check['error'] + "```")
                                    await channel.send("```The bot is leaving [" + server_name + "].```")
                                break

                            await server_info.leave()
                        except Exception as e:
                            for channel in guild.text_channels:
                                if channel.permissions_for(guild.me).send_messages:
                                    await channel.send("```Issue getting server information. " + str(e))
                                break
                    else:
                        for channel in guild.text_channels:
                            if channel.permissions_for(guild.me).send_messages:
                                joining = ""
                                joining += "```I am happy to join this server!```"

                                await channel.send(joining)
                                await asyncio.sleep(1)
                            break
                else:
                    try:
                        server_info = await self.bot.fetch_guild(server_id)
                        for channel in guild.text_channels:
                            if channel.permissions_for(guild.me).send_messages:
                                await channel.send("```Bot cannot be joined. Server seems fresh.```")
                                await channel.send("```The bot is leaving [" + server_name + "].```")
                                await asyncio.sleep(1)
                            break

                        await server_info.leave()
                    except Exception as e:
                        for channel in guild.text_channels:
                            if channel.permissions_for(guild.me).send_messages:
                                await channel.send("```Issue getting server information. " + str(e))
                                await asyncio.sleep(1)
                            break
