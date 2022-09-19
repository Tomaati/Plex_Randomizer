from flask import Flask
from helper import random_media_check_collection, open_media
from config import movies, client, shows

app = Flask(__name__)


@app.route('/movie')
def get_random_media():
    media = random_media_check_collection(movies)
    open_media(client, media)
    return f'Opening: {media.title}...'


@app.route('/show')
def get_random_show():
    media = random_media_check_collection(shows)
    open_media(client, media)
    return f'Opening: {media.title}...'


@app.route('/movie/<genres>')
def get_random_media_genre(genres):
    genres = genres.split(',')
    media = random_media_check_collection(movies, genres)
    open_media(client, media)
    return f'Opening: {media.title}...'


@app.route('/show/<genres>')
def get_random_show_genre(genres):
    genres = genres.split(',')
    media = random_media_check_collection(shows, genres)
    open_media(client, media)
    return f'Opening: {media.title}...'


if __name__ == '__main__':
    app.run()
    # questions = [inquirer.List('MediaType',
    #                            message='What type of media do you want to watch?',
    #                            choices=['Movies', 'TV Shows']),
    #              inquirer.List('GenreYN',
    #                            message='Do you want to filter based on Genre?',
    #                            choices=['Yes', 'No'])
    #              ]
    # answers = inquirer.prompt(questions)
    #
    # media = None
    # genres = None
    #
    # if answers['MediaType'] == 'Movies':
    #     if answers['GenreYN'] == 'Yes':
    #         genres = select_genre(movies)
    #
    #     media = random_media_check_collection(movies, genres)
    #
    # if answers['MediaType'] == 'TV Shows':
    #     if answers['GenreYN'] == 'Yes':
    #         genres = select_genre(shows)
    #
    #     media = random_media_check_collection(shows, genres)
    #
    # print(f'Opening: {media.title}...')
    # open_media(media)
