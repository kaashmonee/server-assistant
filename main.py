from dotenv import load_dotenv
import api_server
import os
import logging
import sys
from bot_def import new_bot


def main():
    api_server.keep_alive()

    # just doing it this way because we're defining this class by overriding the actual methods and also
    # using decorators. just want to do it this way so that we can isolate all the bot configuration code
    # to a single file
    bot = new_bot()

    # load secrets
    DISCORD_BOT_TOKEN_ENV_KEY = "DISCORD_BOT_TOKEN"
    load_dotenv()
    discord_bot_token_value = os.getenv(DISCORD_BOT_TOKEN_ENV_KEY)
    if discord_bot_token_value is None:
        logging.error(
            f"missing .env file or missing variable: {DISCORD_BOT_TOKEN_ENV_KEY}")
        sys.exit(1)

    bot.run(discord_bot_token_value)


if __name__ == "__main__":
    main()
