import discord
from typing import List
import logging
from typing import Union
import re


logging.basicConfig(level=logging.DEBUG,
                    format="[%(pathname)s:%(lineno)d | (%(funcName)s)] %(message)s")


def in_discord_thread(message: discord.Message):
    return isinstance(message.channel, discord.Thread)


def user_id_in_message(user_id: int, message_content: str) -> bool:
    return f"<@{user_id}>" in message_content


def get_hyperlink(message_content: str) -> Union[str, None]:
    """Gets a hyperlink if exists in the message
    https://stackoverflow.com/questions/839994/extracting-a-url-in-python

    Args:
        message_content (str): string from which to extract the url

    Returns:
        str: URL
    """
    regex = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"

    matches: List[str] = re.findall(regex, message_content)
    if len(matches) == 0:
        return None

    return matches[0]


async def get_thread_messages(message: discord.Message, limit=1000) -> str:
    channel = message.channel
    if not in_discord_thread(message):
        logging.info(f"retrieving the last {limit} messages in the channel")

    thread: discord.Thread = channel
    messages: List[str] = []
    async for msg in thread.history(limit=limit):
        messages.append(f"{msg.author.display_name}: {msg.content}")

    # delimit the messages by new lines
    messages_str = "\n".join(messages)
    return messages_str


def assert_value_str(values: List[str]):
    for val in values:
        assert val is not None and val != ""
