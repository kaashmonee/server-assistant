import discord


def in_thread(message: discord.Message) -> bool:
    channel = message.channel
    return isinstance(channel, discord.Thread)
