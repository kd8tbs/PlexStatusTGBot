from plexapi.server import PlexServer
import os
import telegram

# Global variable to store the instance of the Plex server
_plex_server_instance: PlexServer = None




def get_plex_server() -> PlexServer:
    global _plex_server_instance
    if _plex_server_instance is None:
       _plex_server_instance = PlexServer(
            os.getenv('PLEX_SERVER_URL'), os.getenv('PLEX_AUTH_TOKEN'))
    return _plex_server_instance


def get_telegram_bot() -> telegram.Bot:
    return telegram.Bot(os.getenv('TELEGRAM_BOT_TOKEN'))