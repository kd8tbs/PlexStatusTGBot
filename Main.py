# Description: Main file for the bot
# import dependencies for loading environment variables
import telegram
import asyncio
from plexapi.server import PlexServer
import plexapi
import os
import secrets
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
# import dependencies for Plex API
# import dependencies for Telegram API

#Global variable to store the instance of the Plex server
plex_server_instance = None

# Global variable to store the instance of the Telegram bot
telegram_bot_instance = None


def getPlexServer():
    global plex_server_instance
    if plex_server_instance is None:
        plex_server_instance = PlexServer(os.getenv('PLEX_SERVER_URL'), os.getenv('PLEX_AUTH_TOKEN'))
    return plex_server_instance


def getTelegramBot():
    global telegram_bot_instance
    if telegram_bot_instance is None:
        telegram_bot_instance = telegram.Bot(os.getenv('TELEGRAM_BOT_TOKEN'))
    return telegram_bot_instance


# Example 1: List all unwatched movies.
# movies = plex.library.section('Movies')
# for video in movies.search(unwatched=True):
#     print(video.title)

async def main():
    bot = getTelegramBot()
    plex = getPlexServer()
    for video in plex.library.section('Movies').search(unwatched=True):
        await bot.sendMessage(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text=video.title)
    await bot.sendMessage(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text='I did a thing!(watch the movies you download!)')
    await bot.sendMessage(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text='(The Telegram bot uprising will occur soon.)')


if __name__ == '__main__':
    asyncio.run(main())
