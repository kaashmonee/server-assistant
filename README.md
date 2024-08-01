# server-assistant

Discord bot to be able to use different chat backends to be personal assistant in my server.
Start code obtained from @SGtOriginal: https://github.com/SGtOriginal/Making-Discord-Bots. (Ty!)

Note: currently only supports claude3.5

## Getting Started

```bash
cp example.env .env
# Fill in the missing variables
# install missing required packages
python bot.py
```

Example `.env` custom instructions:

```
# keys not shown
SYSTEM_INSTRUCTIONS="You are a helpful discord server assistant and everything you do is in the context of a discord server. You should summarize the content of the message and respond with your best attempt at what it could mean. You should also be cheeky, humorous, and fun.

The messages will be of the following format:

person A: something
person B: something else

where you have the name of the person, a colon, and the message they sent, delimited by a newline. Reference the author names of the messages in your response if appropriate. Don't be overly enthusiastic or anything and do not be cringe."
```

## Next Steps

Help add context to the bot:

1. For each discord message, prepend it with the name of the person saying it and then comma delimit it \[DONE\]
2. Add the format of the input to the custom instructions of the bot \[DONE\]

Usability improvements:
1. Add reply ability to bot: (if you reply to the bot, it'll be able to respond back) \[DONE\]
2. Add custom functions/code to have it scrape/read a website and then summarize the entire link if there exists one

