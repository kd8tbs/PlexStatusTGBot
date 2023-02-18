# Description: Main file for the bot
# import dependencies for loading environment variables
import os
import secrets
from pathlib import Path
from dotenv import load_dotenv

import plexapi
from plexapi.server import PlexServer
load_dotenv()

baseurl = os.getenv('PLEX_SERVER_URL')
token = os.getenv('PLEX_AUTH_TOKEN')
plex = PlexServer(baseurl, token)
# Example 1: List all unwatched movies.
movies = plex.library.section('Movies')
for video in movies.search(unwatched=True):
    print(video.title)