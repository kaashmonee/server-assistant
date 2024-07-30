import discord
from typing import List


async def get_thread_messages(message: discord.Message) -> str:
    channel = message.channel
    if not isinstance(channel, discord.Thread):
        raise TypeError(f"channel type: {channel}, expected discord.Thread")

    thread: discord.Thread = channel
    messages: List[str] = []
    async for msg in thread.history(limit=None):
        messages.append(f"{msg.author.display_name}: {msg.content}")

    # delimit the messages by new lines
    messages_str = "\n".join(messages)
    return messages_str
