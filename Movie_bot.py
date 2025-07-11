import os
from dotenv import find_dotenv, load_dotenv
import telebot
import json
from itertools import islice
from PyMovieDb import IMDB

imdb = IMDB()

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

# List of allowed genres (used for input validation)
VALID_GENRES = {
    'Action', 'Adventure', 'Animation', 'Biography', 'Comedy',
    'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy',
    'Horror', 'History', 'Mystery', 'Music', 'Romance',
    'Sport', 'Thriller'
}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome = (
        "Hi Movie Buff!\n"
        "To know the currently most popular movies or TV shows on IMDb, click any of these:\n"
        "/movies - Top movies by genre\n"
        "/tv - Top TV shows by genre"
    )
    bot.reply_to(message, welcome)


@bot.message_handler(commands=['movies'])
def movie_genre(message):
    msg = (
        "To get the top movies of a specific genre, please type one of the following genres:\n\n"
        + "\n".join(sorted(VALID_GENRES))
    )
    sent_msg = bot.send_message(message.chat.id, msg, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, info_str1)



@bot.message_handler(commands=['tv'])
def tv_genre(message):
    msg = (
        "To get the top TV shows of a specific genre, please type one of the following genres:\n\n"
        + "\n".join(sorted(VALID_GENRES))
    )
    sent_msg = bot.send_message(message.chat.id, msg, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, info_str2)



def fetch_and_send_titles(chat_id, response):
    
    try:
        data = json.loads(response)
        titles_string = ""
        for i, item in enumerate(islice(data['results'], 20), start=1):
            name = item.get('name', 'Unknown')
            year = item.get('year', 'N/A')
            url = item.get('url', 'N/A')
            titles_string += f"{i}. {name} ({year}) - {url}\n"
        bot.send_message(chat_id, titles_string)
    except Exception as e:
        bot.send_message(chat_id, "Error while processing data.")
        print("JSON Parse Error:", e)


def info_str1(message):
    gen = message.text.title()
    if gen not in VALID_GENRES:
        bot.send_message(message.chat.id, "Invalid genre. Please use /movies to try again.")
        return
    try:
        response = imdb.popular_movies(genre=gen, start_id=0, sort_by='Popularity')
        fetch_and_send_titles(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Failed to fetch movie data.")
        print("Movie fetch error:", e)



def info_str2(message):
    gen = message.text.title()
    if gen not in VALID_GENRES:
        bot.send_message(message.chat.id, "Invalid genre. Please use /tv to try again.")
        return
    try:
        response = imdb.popular_tv(genre=gen, start_id=0, sort_by='Popularity')
        fetch_and_send_titles(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Failed to fetch TV show data.")
        print("TV fetch error:", e)



bot.infinity_polling()