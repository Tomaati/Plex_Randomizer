import random
import inquirer
import configparser

from plexapi.server import PlexServer
from plexapi.library import ShowSection


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


def get_all_media_filter_watch(library, unwatched=True, genre=None):
    if genre is not None:
        return library.search(unwatched=unwatched, genre=genre)
    return library.search(unwatched=unwatched)


def get_random_media_unwatched(library, genre):
    return random.choice(get_all_media_filter_watch(library, genre=genre))


def first_unplayed_collection(collection):
    for movie in collection:
        if not movie.viewCount:
            return movie


def random_media_check_collection(library, genre):
    movie = get_random_media_unwatched(library, genre)
    collections = movie.collections

    if not collections:
        return movie
    else:
        collection = collections[0].collection()
        return first_unplayed_collection(collection.items())


def open_media(media):
    client.goToMedia(media)


def select_genre(library):
    questions = [
        inquirer.Checkbox('genre',
                          message='What Genre do you want to watch?',
                          choices=show_genres if isinstance(library, ShowSection) else movie_genres)
        ]
    answers = inquirer.prompt(questions)
    return answers['genre']


if __name__ == '__main__':
    questions = [inquirer.List('MediaType',
                               message='What type of media do you want to watch?',
                               choices=['Movies', 'TV Shows']),
                 inquirer.List('GenreYN',
                               message='Do you want to filter based on Genre?',
                               choices=['Yes', 'No'])
                 ]
    answers = inquirer.prompt(questions)

    media = None
    genres = None

    if answers['MediaType'] == 'Movies':
        if answers['GenreYN'] == 'Yes':
            genres = select_genre(movies)

        media = random_media_check_collection(movies, genres)

    if answers['MediaType'] == 'TV Shows':
        if answers['GenreYN'] == 'Yes':
            genres = select_genre(shows)

        media = random_media_check_collection(shows, genres)

    print(f'Opening: {media.title}...')
    open_media(media)
