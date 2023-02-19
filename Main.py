# Description: Main file for the bot
# import dependencies for loading environment variables
import telegram
import asyncio
from plexapi.server import PlexServer
import plexapi
import os
from dotenv import load_dotenv
from time import sleep

# Global variable to store the instance of the Plex server
plex_server_instance = None

# Global variable to store the instance of the Telegram bot
telegram_bot_instance = None


def getPlexServer():
    global plex_server_instance
    if plex_server_instance is None:
        plex_server_instance = PlexServer(
            os.getenv('PLEX_SERVER_URL'), os.getenv('PLEX_AUTH_TOKEN'))
    return plex_server_instance


def getTelegramBot():
    global telegram_bot_instance
    if telegram_bot_instance is None:
        telegram_bot_instance = telegram.Bot(os.getenv('TELEGRAM_BOT_TOKEN'))
    return telegram_bot_instance


def isPlexOnline():
    try:
        getPlexServer().clients()
        return True
    except:
        return False


async def main():
    bot = getTelegramBot()
    plex = getPlexServer()
    await bot.sendMessage(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text='Test message from PlexBot')

    # TODO: move this to a separate function and parallelize it    
    is_plex_online = True  # Start with Plex server assumed to be online

    while True:
        print('Checking if Plex is online...')
        if isPlexOnline():
            if not is_plex_online:
                await bot.sendMessage(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text='Plex is now online!')
                print('Plex is online! Message sent to Telegram')
            is_plex_online = True
        else:
            if is_plex_online:
                await bot.sendMessage(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text='Plex is now offline!')
                print('Plex is offline! Message sent to Telegram')
            is_plex_online = False
        sleep(10)


if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main())
