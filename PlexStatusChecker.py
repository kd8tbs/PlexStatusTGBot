import telegram
import os
import asyncio
import threading
from time import sleep
from utils import get_plex_server, get_telegram_bot

class PlexStatusThread():

    def __init__(self, bot_instance):
        self.bot_instance = bot_instance
        self.stopped = False

    async def main(self):
        await self.bot_instance.sendMessage(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text='Plex Status Checker is now online')
        print('Plex Status Checker is now online')

        # run check_plex_status() in the background
        asyncio.create_task(self.check_plex_status())

        while not self.stopped:
            await asyncio.sleep(1)
    
    def is_plex_online(self):
        try:
            # TODO: Find a better way to check if Plex is online. This could probably just be a simple ping.
            get_plex_server().clients()
            return True
        except ConnectionError:
            return False
        except Exception as e:
            print('Error checking if Plex is online: ' + str(e))
            return False

    async def check_plex_status(self):
        # TODO: Figure out how to not assume Plex is online at the start
        plex_status = True  # Start with Plex server assumed to be online

        while True:
            print('Checking if Plex is online...')
            if self.is_plex_online():
                if not plex_status:
                    await self.bot_instance.sendMessage(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text='Plex is now online!')
                    print('Plex is online! Message sent to Telegram')
                plex_status = True
            else:
                if plex_status:
                    await self.bot_instance.sendMessage(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text='Plex is now offline!')
                    print('Plex is offline! Message sent to Telegram')
                plex_status = False
            sleep(10)

    def run_thread(self):
        asyncio.run(self.main())

    # Starts main thread
    def start_thread(self):
        self.thread: threading.Thread = threading.Thread(target=self.run_thread, daemon=True)
        self.thread.start()

    def stop_thread(self):
        self.stopped = True
        self.thread.join()