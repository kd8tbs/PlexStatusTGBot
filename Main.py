# Description: Main file for the bot
from dotenv import load_dotenv
from PlexStatusChecker import PlexStatusThread
from TelegramFunctions import TelegramFunctions
from utils import get_telegram_bot

if __name__ == '__main__':
    load_dotenv()

    # TODO: Figure out how to make these run simultaneously
    # TODO: Probably decouple these into their own files?
    status_thread: PlexStatusThread = PlexStatusThread(get_telegram_bot())
    status_thread.start_thread()

    application: TelegramFunctions = TelegramFunctions(get_telegram_bot())
    application.run()
