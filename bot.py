from dotenv import load_dotenv
import random
import discord
from discord.ext import commands
import api_server
import os
import logging
import utils
import sys
import llm_backend

bot = commands.Bot(command_prefix=commands.when_mentioned_or(
    "!"), intents=discord.Intents.all())

logging.basicConfig(level=logging.DEBUG,
                    format="[%(pathname)s:%(lineno)d | (%(funcName)s)] %(message)s")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("still not fucking working"))

    logging.info(f"Connected to bot: {bot.user.name}")
    logging.info(f"Bot ID: {bot.user.id}")


@bot.command()
async def summarize(ctx: commands.Context):
    logging.info("command started")
    message: discord.Message = ctx.message

    # try:
    thread_messages_str = await utils.get_thread_messages(message)
    # except Exception as e:
    #     logging.info(f"caused exception: {e}")
    #     await ctx.send(f"failed with error: {e}")
    #     return

    client = llm_backend.Client("claude")
    response = await client.send_in_thread(thread_messages_str)
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

api_server.keep_alive()

# load secrets
DISCORD_BOT_TOKEN_ENV_KEY = "DISCORD_BOT_TOKEN"
load_dotenv()
discord_bot_token_value = os.getenv(DISCORD_BOT_TOKEN_ENV_KEY)
if discord_bot_token_value is None:
    logging.error(
        f"missing .env file or missing variable: {DISCORD_BOT_TOKEN_ENV_KEY}")
    sys.exit(1)

bot.run(discord_bot_token_value)
