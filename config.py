import configparser

from plexapi.server import PlexServer

config = configparser.RawConfigParser()
config.read('config.cfg')

plex_information = dict(config.items('SERVER_INFORMATION'))
plex = PlexServer(plex_information['baseurl'], plex_information['token'])

library_information = dict(config.items('LIBRARY_INFORMATION'))
movies = plex.library.section(library_information['movie_library'])
shows = plex.library.section(library_information['show_library'])

genre_information = dict(config.items('GENRES'))
movie_genres = genre_information['movie_genres'].split(',')
show_genres = genre_information['show_genres'].split(',')

client_information = dict(config.items('CLIENT_INFORMATION'))
client = plex.client(client_information['client_name'])