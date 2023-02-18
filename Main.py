# Description: Main file for the bot
# import dependencies for loading environment variables
import os
import secrets
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
# import dependencies for Plex API
import plexapi
from plexapi.server import PlexServer
# import dependencies for Telegram API
import asyncio
import telegram


def getPlexServer():
    return PlexServer(os.getenv('PLEX_SERVER_URL'), os.getenv('PLEX_AUTH_TOKEN'))

def getTelegramBot():
    return telegram.Bot(os.getenv('TELEGRAM_BOT_TOKEN'))



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