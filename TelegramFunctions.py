import telegram
import os
import random
import threading
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram import Update
from utils import get_plex_server


class TelegramFunctions():

    def __init__(self, bot_instance):
        self.bot_instance: telegram.Bot = bot_instance

        self._application: ApplicationBuilder = ApplicationBuilder().token(
        os.getenv('TELEGRAM_BOT_TOKEN')).build()

        # function handlers go here
        start_handler = CommandHandler('start', self.start)
        self._application.add_handler(start_handler)

        get_random_movie_handler = CommandHandler('getRandomMovie', self.get_random_movie)
        self._application.add_handler(get_random_movie_handler)

    def run(self):
        print("Starting command listener...")
        self._application.run_polling()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You started me! :D")

    async def get_random_movie(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        movies = get_plex_server().library.section('Movies').all()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(movies).title)
