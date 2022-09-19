import random
import inquirer

from plexapi.library import ShowSection
from config import show_genres, movie_genres


def get_all_media_filter_watch(library, unwatched=True, genre=None):
    if genre is not None:
        return library.search(unwatched=unwatched, genre=genre)
    return library.search(unwatched=unwatched)


def get_random_media_unwatched(library, genre=None):
    return random.choice(get_all_media_filter_watch(library, genre=genre))


def first_unplayed_collection(collection):
    for movie in collection:
        if not movie.viewCount:
            return movie


def random_media_check_collection(library, genre=None):
    movie = get_random_media_unwatched(library, genre)
    collections = movie.collections

    if not collections:
        return movie
    else:
        collection = collections[0].collection()
        return first_unplayed_collection(collection.items())


def open_media(client, media):
    client.goToMedia(media)


def select_genre(library):
    questions = [
        inquirer.Checkbox('genre',
                          message='What Genre do you want to watch?',
                          choices=show_genres if isinstance(library, ShowSection) else movie_genres)
    ]
    answers = inquirer.prompt(questions)
    return answers['genre']
