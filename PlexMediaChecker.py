import time
import telegram
import os
import asyncio
import threading
from time import sleep
from utils import get_plex_server, get_telegram_bot

class PlexMediaThread():

    def __init__(self, bot_instance):
        self.bot_instance = bot_instance
        self.stopped = False

    async def main(self):
        await self.bot_instance.sendMessage(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text='Plex Media Checker is now online')
        print('Plex Media Checker is now online')

        # run check_new_media() in the background
        asyncio.create_task(self.check_new_media())

        while not self.stopped:
            await asyncio.sleep(1)
    
    async def check_new_media(self):
        # TODO: Make this not sned the most recent item on startup
        plex = get_plex_server()

        # Get the library section for TV Shows and Movies
        tv_shows = plex.library.section('TV Shows')
        movies = plex.library.section('Movies')

        # Keep track of the most recent item added for each library section
        most_recent_tv = None
        most_recent_movie = None

        while True:
            # Get the most recent item in the TV Shows library section
            tv_item = tv_shows.recentlyAdded()[0]

            # If the most recent item is different than the previous most recent item,
            # print a message indicating that new media has been added
            if tv_item != most_recent_tv:
                print(f"New TV show added: {tv_item.title}")
                await self.bot_instance.sendMessage(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text=f"New TV show added: {tv_item.title} ({tv_item.year})")
                most_recent_tv = tv_item

            # Get the most recent item in the Movies library section
            movie_item = movies.recentlyAdded()[0]

            # If the most recent item is different than the previous most recent item,
            # print a message indicating that new media has been added
            if movie_item != most_recent_movie:
                print(f"New movie added: {movie_item.title}")
                await self.bot_instance.sendMessage(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text=f"New movie added: {movie_item.title} ({movie_item.year})")
                most_recent_movie = movie_item

            # Wait for 10 seconds before checking for new media again
            time.sleep(10)
    
    def run_thread(self):
        asyncio.run(self.main())
    
    # Starts main thread
    def start_thread(self):
        self.thread: threading.Thread = threading.Thread(target=self.run_thread, daemon=True)
        self.thread.start()
    
    def stop_thread(self):
        self.stopped = True
        self.thread.join()