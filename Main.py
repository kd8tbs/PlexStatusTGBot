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


def get_plex_server():
    global plex_server_instance
    if plex_server_instance is None:
        plex_server_instance = PlexServer(
            os.getenv('PLEX_SERVER_URL'), os.getenv('PLEX_AUTH_TOKEN'))
    return plex_server_instance


def get_telegram_bot():
    global telegram_bot_instance
    if telegram_bot_instance is None:
        telegram_bot_instance = telegram.Bot(os.getenv('TELEGRAM_BOT_TOKEN'))
    return telegram_bot_instance


def is_plex_online():
    try:
        get_plex_server().clients() # TODO: Find a better way to check if Plex is online. This could probably just be a simple ping.
        return True
    except:
        return False


async def check_plex_status():
    plex_status = True  # Start with Plex server assumed to be online

    while True:
        print('Checking if Plex is online...')
        if is_plex_online():
            if not plex_status:
                await get_telegram_bot().sendMessage(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text='Plex is now online!')
                print('Plex is online! Message sent to Telegram')
            plex_status = True
        else:
            if plex_status:
                await get_telegram_bot().sendMessage(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text='Plex is now offline!')
                print('Plex is offline! Message sent to Telegram')
            plex_status = False
        sleep(10)


async def main():
    await get_telegram_bot().sendMessage(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text='Plex Bot is now online')

    # run checkPlexStatus() in the background
    checkPlexStatusTask = asyncio.create_task(check_plex_status())

    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main())
