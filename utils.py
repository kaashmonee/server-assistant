import discord
from typing import List
import logging


logging.basicConfig(level=logging.DEBUG,
                    format="[%(pathname)s:%(lineno)d | (%(funcName)s)] %(message)s")


def in_discord_thread(message: discord.Message):
    return isinstance(message.channel, discord.Thread)


def user_id_in_message(user_id: int, message_content: str) -> bool:
    return f"<@{user_id}>" in message_content


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
