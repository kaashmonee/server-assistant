import random
import discord
from discord.ext import commands
import logging
import llm_backend
import utils
from typing import Dict

logging.basicConfig(level=logging.DEBUG,
                    format="[%(pathname)s:%(lineno)d | (%(funcName)s)] %(message)s")


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.llm_client = llm_backend.Client("claude")
        self.threads: Dict[str, str] = {}

    async def _is_command(self, message: discord.Message):
        # assume there's only one prefix string
        cmd_prefix_string = await self.get_prefix(message)
        valid_commands = self.all_commands.keys()
        for cmd_name in valid_commands:
            if message.content.startswith(cmd_prefix_string+cmd_name):
                return True

        return False

    async def on_message(self, message: discord.Message):
        """Slightly modify the on_message handler to trigger commands. If not commands were triggered, 
        proceed to handle the message

        Args:
            message (discord.Message): Message event handler: message to respond to
        """
        logging.info(
            f"author: {message.author.display_name}, message: {message.content}")

        # just calls process_commands
        if await self._is_command(message):
            logging.debug("not a command")
            await self.process_commands(message)
            return

        if not utils.user_id_in_message(self.user.id, message.content):
            logging.info("no need to do anything with the message")
            return

        thread_messages: str = await utils.get_thread_messages(message, limit=1)

        # this means that the bot was mentioned
        # send this message to the AI in the corresponding thread/channel
        discord_messageable_interface_id = str(message.channel.id)
        if discord_messageable_interface_id not in self.threads:
            self.threads[discord_messageable_interface_id] = []

        self.threads[discord_messageable_interface_id].append(
            f"{message.author.display_name}: {message.content}")

        async with message.channel.typing():
            llm_response: str = await self.llm_client.send_in_thread(thread_messages, thread_id=discord_messageable_interface_id)

        await message.reply(llm_response)


def new_bot() -> Bot:
    bot: Bot = Bot(command_prefix="!", intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        await bot.change_presence(activity=discord.Game("with your mom"))

        logging.info(f"Connected to bot: {bot.user.name}")
        logging.info(f"Bot ID: {bot.user.id}")

        bot.llm_client.set_bot_name(bot.user.name)

    @bot.command()
    async def summarize(ctx: commands.Context):
        logging.info("summarize command called")
        message: discord.Message = ctx.message

        try:
            thread_messages_str = await utils.get_thread_messages(message)
        except TypeError:
            await ctx.send("sorry, but i can only summarize threads!")
            return

        async with ctx.typing():
            response = await bot.llm_client.send_in_thread(thread_messages_str)

        await ctx.send(response)

    @bot.command(
        help="Uses come crazy logic to determine if pong is actually the correct value or not.",
        brief="Prints pong back to the channel."
    )
    async def ping(ctx):
        await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

    @bot.command()
    async def hello(ctx):
        await ctx.send(f'Hi!')

    @bot.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, a: int):
        await ctx.channel.purge(limit=1 + a)
        await ctx.send(f'Channel cleared!')

    @bot.command(
        help="Changes the nickname.",
        brief="The name says it all."
    )
    async def nick(ctx, member: discord.Member, args):
        await member.edit(nick=args)
        await ctx.send(f'Nickname changed.')

    @bot.command(
        help="Looks like you need some help, lol.",
        brief="Prints the list of values back to the channel."
    )
    async def print(ctx, *args):
        response = ""
        for arg in args:
            response = response + " " + arg
        await ctx.channel.send(response)

    @bot.command(
        help="Add numbers like this 'add 10 20'.",
        brief="Add numbers like this 'add 10 20'."
    )
    async def add(ctx, a: int, b: int):
        await ctx.send(a + b)

    @bot.command(
        help="Subtract numbers like this 'sub 10 20'.",
        brief="Subtract numbers like this 'sub 10 20'."
    )
    async def sub(ctx, a: int, b: int):
        await ctx.send(a - b)

    @bot.command(
        help="Multiplies numbers like this 'mul 10 20'.",
        brief="Multiplies numbers like this 'mul 10 20'."
    )
    async def mul(ctx, a: int, b: int):
        await ctx.send(a * b)

    @bot.command(
        help="Divide numbers like this 'div 10 20'.",
        brief="Divide numbers like this 'div 10 20'."
    )
    async def div(ctx, a: int, b: int):
        await ctx.send(a / b)

    @bot.command(
        help="Chooses between two options.",
        brief="Chooses between two options."
    )
    async def choose(ctx, a: str, b: str):
        list1 = [a, b]
        await ctx.send(random.choice(list1))

    return bot
