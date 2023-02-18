# Description: Main file for the bot
# import dependencies for loading environment variables
import os
import secrets
from pathlib import Path
from dotenv import load_dotenv

# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API
import asyncio
import telegram



async def main():
    load_dotenv(verbose=True)

    bot = telegram.Bot(os.getenv('TELEGRAM_BOT_TOKEN'))
    async with bot:
        print((await bot.get_me()))
        print((await bot.get_updates())[0])


if __name__ == '__main__':
    asyncio.run(main())
