import requests
from core.EnvParser import EnvParser
from from_root import from_root
from core.Logger import Logger
from datetime import datetime, timedelta
import time
from functools import wraps
from typing import Union


class Embed:
    def __init__(self):
        self.embed = {"title": None, "description": None, "color": None, "fields": []}

    def set_title(self, title: str):
        self.embed["title"] = title
        return self

    def set_description(self, description: str):
        self.embed["description"] = description
        return self

    def set_color(self, color: int):
        self.embed["color"] = color
        return self

    def add_field(self, name: str, value: str, inline: bool = False):
        field = {"name": name, "value": value, "inline": inline}
        self.embed["fields"].append(field)
        return self

    def build(self):
        return self.embed


class ApiActions:
    DISCORD_EPOCH = 1420070400000
    MAX_RETRIES = 5
    RETRY_DELAY = 2

    def __init__(self) -> None:
        env = EnvParser(from_root(".env"))
        self.api_base_url = "https://discord.com/api/v10"
        self.bot_token = env.get("BOT_TOKEN")
        self.logger = Logger("API Actions").get_logger()

    def retry_request(func):
        """Decorator to retry request on failure or rate-limiting (429)."""

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            retries = 0
            while retries < self.MAX_RETRIES:
                try:
                    response = func(self, *args, **kwargs)

                    if response.status_code in [200, 201, 204]:
                        return {"status": True}
                    elif response.status_code == 429:
                        retry_after = response.json().get(
                            "retry_after", self.RETRY_DELAY
                        )
                        self.logger.warning(
                            f"Rate limited, retrying in {retry_after} seconds..."
                        )
                        time.sleep(retry_after)
                    else:
                        self.logger.error(
                            f"Failed to send request: {response.status_code} - {response.text}"
                        )
                        return {
                            "status": False,
                            "code": response.status_code,
                            "error": f"{response.status_code} - {response.text}",
                        }

                except requests.RequestException as e:
                    self.logger.error(f"Request error while sending message: {e}")
                    return {"status": False, "error": f"Error: {e}"}

                retries += 1
                time.sleep(self.RETRY_DELAY)
            return {"status": False, "error": "Max retries reached"}

        return wrapper

    def get_age_in_days_from_id(self, entity_id: int) -> int:
        """Extract the user creation date from the Discord Snowflake ID and return the account age in days."""
        timestamp = ((entity_id >> 22) + self.DISCORD_EPOCH) / 1000
        creation_date = datetime.utcfromtimestamp(timestamp)

        current_date = datetime.utcnow()
        age_in_days = (current_date - creation_date).days

        return age_in_days

    @retry_request
    def send_message_to_channel(self, channel_id: int, data: any):
        """Send logs to a Discord channel."""
        url = f"{self.api_base_url}/channels/{channel_id}/messages"
        payload = {"content": f"```{data}```"}
        return requests.post(
            url,
            headers={
                "Authorization": f"Bot {self.bot_token}",
                "Content-Type": "application/json",
            },
            json=payload,
        )

    @retry_request
    def send_dm(self, user_id: int, data: any):
        """Send a direct message to a user."""
        url = f"{self.api_base_url}/users/{user_id}/messages"
        payload = {"content": f"```{data}```"}
        return requests.post(
            url,
            headers={
                "Authorization": f"Bot {self.bot_token}",
                "Content-Type": "application/json",
            },
            json=payload,
        )

    @retry_request
    def send_embed_to_channel(self, channel_id: int, embed: dict):
        """Send an embed message to a Discord channel."""
        url = f"{self.api_base_url}/channels/{channel_id}/messages"
        payload = {"embeds": [embed]}
        return requests.post(
            url,
            headers={
                "Authorization": f"Bot {self.bot_token}",
                "Content-Type": "application/json",
            },
            json=payload,
        )

    @retry_request
    def send_embed_to_dm(self, user_id: int, embed: dict):
        """Send an embed message to a user's DM."""
        url = f"{self.api_base_url}/users/{user_id}/messages"
        payload = {"embeds": [embed]}
        return requests.post(
            url,
            headers={
                "Authorization": f"Bot {self.bot_token}",
                "Content-Type": "application/json",
            },
            json=payload,
        )

    @retry_request
    def delete_message(self, channel_id: int, message_id: int):
        """
        Delete a single message from a channel.
        :param channel_id: The ID of the channel.
        :param message_id: The ID of the message to delete.
        """
        url = f"{self.api_base_url}/channels/{channel_id}/messages/{message_id}"
        return requests.delete(
            url,
            headers={
                "Authorization": f"Bot {self.bot_token}",
                "Content-Type": "application/json",
            },
        )

    @retry_request
    def ban_user(
        self, guild_id: int, user_id: int, reason: str = None, delete_days: int = 7
    ):
        """
        Ban a user from the guild.
        :param guild_id: The ID of the guild (server).
        :param user_id: The ID of the user to be banned.
        :param reason: The reason for banning the user.
        :param delete_days: Number of days of messages to delete (0-7).
        """
        url = f"{self.api_base_url}/guilds/{guild_id}/bans/{user_id}"
        payload = {"delete_message_days": delete_days, "reason": reason}
        return requests.put(
            url,
            headers={
                "Authorization": f"Bot {self.bot_token}",
                "Content-Type": "application/json",
            },
            json=payload,
        )

    @retry_request
    def kick_user(self, guild_id: int, user_id: int, reason: str = None):
        """
        Kick a user from a guild (server).
        :param guild_id: The ID of the guild (server) from which to kick the user.
        :param user_id: The ID of the user to kick.
        :param reason: Optional reason for kicking the user.
        """
        url = f"{self.api_base_url}/guilds/{guild_id}/members/{user_id}"

        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "Content-Type": "application/json",
        }

        if reason:
            headers["X-Audit-Log-Reason"] = reason

        return requests.delete(url, headers=headers)

    @retry_request
    def timeout_user(
        self, guild_id: int, user_id: int, duration_in_minutes: int, reason: str = None
    ):
        url = f"{self.api_base_url}/guilds/{guild_id}/members/{user_id}"

        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "Content-Type": "application/json",
        }

        if reason:
            headers["X-Audit-Log-Reason"] = reason

        timeout_end = datetime.utcnow() + timedelta(minutes=duration_in_minutes)
        timeout_end_iso = timeout_end.isoformat() + "Z"

        payload = {"communication_disabled_until": timeout_end_iso}
        return requests.patch(url, json=payload, headers=headers)

    def get_guild_members(self, guild_id: int, limit: int = 1000, after: int = None):
        """Retrieve the list of guild members from a Discord server."""
        url = f"{self.api_base_url}/guilds/{guild_id}/members"

        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "Content-Type": "application/json",
        }

        params = {"limit": limit}
        if after:
            params["after"] = after

        try:
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                members = response.json()
                self.logger.info(
                    f"Retrieved {len(members)} members from guild {guild_id}."
                )
                return {"status": True, "members": members}
            else:
                self.logger.error(
                    f"Failed to get members: {response.status_code} - {response.text}"
                )
                return {
                    "status": False,
                    "error": f"{response.status_code} - {response.text}",
                }

        except requests.RequestException as e:
            self.logger.error(f"Request error while fetching guild members: {e}")
            return {"status": False, "error": f"Error: {e}"}

    def get_all_guild_members(
        self, guild_id: int, delay: Union[int, float] = 1
    ) -> dict:
        """Fetch all members of a guild, handling pagination automatically, and respect rate limits with a delay."""
        all_members = []
        after = None

        while True:
            response = self.get_guild_members(guild_id, after=after)

            if response["status"]:
                members = response["members"]
                all_members.extend(members)

                if len(members) < 1000:
                    self.logger.info(
                        f"Retrieved all members from guild {guild_id}. Total: {len(all_members)} members."
                    )
                    break

                after = members[-1]["user"]["id"]
                self.logger.info(
                    f"Fetched {len(members)} members, continuing to next batch..."
                )

                self.logger.info(
                    f"Sleeping for {delay} second(s) to respect rate limits..."
                )
                time.sleep(delay)
            else:
                self.logger.error(f"Error fetching members: {response['error']}")
                break

        return (
            {"status": True, "members": all_members}
            if all_members
            else {"status": False, "error": "No members retrieved"}
        )

    def delete_all_invites(self, guild_id: int):
        """
        Delete all invites for a server (guild).
        :param guild_id: The ID of the guild (server).
        """
        url = f"{self.api_base_url}/guilds/{guild_id}/invites"

        try:
            response = requests.get(
                url,
                headers={
                    "Authorization": f"Bot {self.bot_token}",
                    "Content-Type": "application/json",
                },
            )

            if response.status_code == 200:
                invites = response.json()

                for invite in invites:
                    invite_code = invite["code"]
                    delete_url = f"{self.api_base_url}/invites/{invite_code}"

                    delete_response = requests.delete(
                        delete_url,
                        headers={
                            "Authorization": f"Bot {self.bot_token}",
                            "Content-Type": "application/json",
                        },
                    )

                    if delete_response.status_code == 200:
                        self.logger.success(f"Invite {invite_code} deleted.")
                    else:
                        self.logger.error(
                            f"Failed to delete invite {invite_code}: {delete_response.status_code} - {delete_response.text}"
                        )

                    time.sleep(0.5)

                self.logger.info(f"Processed {len(invites)} for {guild_id}")
                return {"status": True}
            else:
                self.logger.error(
                    f"Failed to fetch invites: {response.status_code} - {response.text}"
                )
                return {
                    "status": False,
                    "error": f"{response.status_code} - {response.text}",
                }
        except requests.RequestException as e:
            self.logger.error(f"Request error while deleting invites: {e}")
            return {"status": False, "error": f"Error: {e}"}

    @retry_request
    def leave_guild(self, guild_id: int):
        """
        Leave a Discord guild (server).
        :param guild_id: The ID of the guild to leave.
        """
        url = f"{self.api_base_url}/users/@me/guilds/{guild_id}"
        return requests.delete(
            url,
            headers={
                "Authorization": f"Bot {self.bot_token}",
            },
        )
