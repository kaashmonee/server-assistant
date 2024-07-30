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

## Next Steps

Help add context to the bot:

1. For each discord message, prepend it with the name of the person saying it and then comma delimit it
2. Add the format of the input to the custom instructions of the bot

Usability improvements:
1. Add reply ability to bot: (if you reply to the bot, it'll be able to respond back)
2. Add custom functions/code to have it scrape/read a website and then summarize the entire link if there exists one

