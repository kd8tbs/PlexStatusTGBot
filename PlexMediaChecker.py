import telegram
import os
import asyncio
import threading
from time import sleep
from utils import get_plex_server, get_telegram_bot

class PlexMediaThread():

    def __init__(self):
        self.stopped = False

    async def main(self):
        # blows up and sleep does not fix it
        # maybe telegram api does not like being called from multiple threads? Look into multiple bot instances maybe?
        await get_telegram_bot().sendMessage(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text='Plex Media Checker is now online')
        print('Plex Media Checker is now online')

        # run check_new_media() in the background
        asyncio.create_task(self.check_new_media())

        while not self.stopped:
            await asyncio.sleep(1)
    
    async def check_new_media(self):
        # TODO: implement
        return
    
    def run_thread(self):
        asyncio.run(self.main())
    
    # Starts main thread
    def start_thread(self):
        self.thread: threading.Thread = threading.Thread(target=self.run_thread, daemon=True)
        self.thread.start()
    
    def stop_thread(self):
        self.stopped = True
        self.thread.join()