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




@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    
    welcome= "Hi Movie Buff !\nTo know the currently most popular movies or tv shows on IMDb click any of this :\n/movies or /tv"
    
    bot.reply_to(message, welcome)

@bot.message_handler(commands=['movies']) 
def movie_genre(message):
   
   msg="To know top Movies of specific genre,message me the genre.\n\nAvailable Movie genres:\n\tAction,\n\tAdventure,\n\tAnimation,\n\tBiography,\n\tComedy,\n\tCrime,\n\tDocumentary,\n\tDrama,\n\tFamily,\n\tFantasy,\n\tHorror,\n\tHistory,\n\tMystery,\n\tMusic,\n\tRomance,\n\tSport,\n\tThriller\n"
   sent_msg = bot.send_message(message.chat.id, msg, parse_mode="Markdown")
   bot.register_next_step_handler(sent_msg, info_str1)
      
@bot.message_handler(commands=['tv']) 
def tv_genre(message):
   
   msg="To know top tv shows of specific genre,message me the genre.\n\nAvailable Movie genres:\n\tAction,\n\tAdventure,\n\tAnimation,\n\tBiography,\n\tComedy,\n\tCrime,\n\tDocumentary,\n\tDrama,\n\tFamily,\n\tFantasy,\n\tHorror,\n\tHistory,\n\tMystery,\n\tMusic,\n\tRomance,\n\tSport,\n\tThriller\n"
   sent_msg = bot.send_message(message.chat.id, msg, parse_mode="Markdown")
   bot.register_next_step_handler(sent_msg, info_str2)

def info_str1(message):
    genre = message.text
    gen = genre.title()
    response = imdb.popular_movies(genre=gen, start_id=0, sort_by='Popularity')

    data = json.loads(response)
    

    titles_string =""  
    for i, movie in enumerate(islice(data['results'],20),start=1):
        name = movie.get('name', 'Unknown')
        year = movie.get('year', 'N/A')
        url = movie.get('url', 'N/A')
        
        titles_string+=f"{i}. {name}  ({year}) - ({url})\n"
    # titles_string=gen
    bot.send_message(message.chat.id, titles_string)
   
def info_str2(message):
    genre = message.text
    gen = genre.title()
    response = imdb.popular_tv(genre=gen, start_id=0, sort_by='Popularity')

    data = json.loads(response)
    

    titles_string =""  
    for i, movie in enumerate(islice(data['results'],20),start=1):
        name = movie.get('name', 'Unknown')
        year = movie.get('year', 'N/A')
        url = movie.get('url', 'N/A')
        
        titles_string+=f"{i}. {name}  ({year}) - ({url})\n"
    # titles_string=gen
    bot.send_message(message.chat.id, titles_string)





bot.infinity_polling()