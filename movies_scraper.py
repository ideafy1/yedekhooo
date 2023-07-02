import os
import requests
import bs4
import pyTelegramBotAPI

API_KEY: '29996160'
BOT_TOKEN: '6012981536:AAFrBkIIuA_e23tUwXkIzZ8Gh9FHRCm1E_E'
CHANNEL_ID: '-1983289315'

def search_movies(query):
    movies_list = []
    movies_details = {}
    api_key = os.environ['API_KEY']
    bot = pyTelegramBotAPI.Bot(token=os.environ['BOT_TOKEN'])
    response = bot.get_messages(chat_id=os.environ['CHANNEL_ID'], query=query)
    for movie in response:
        if movie:
            movies_details["id"] = f"link{movies.index(movie)}"
            movies_details["title"] = movie.find("span", {'class': 'mli-info'}).text
            url_list[movies_details["id"]] = movie['href']
        movies_list.append(movies_details)
        movies_details = {}
    return movies_list


def get_movie(query):
    movie_details = {}
    movie_page_link = BeautifulSoup(requests.get(f"{url_list[query]}").text, "html.parser")
    if movie_page_link:
        title = movie_page_link.find("div", {'class': 'mvic-desc'}).h3.text
        movie_details["title"] = title
        img = movie_page_link.find("div", {'class': 'mvic-thumb'})['data-bg']
        movie_details["img"] = img
        links = movie_page_link.find_all("a", {'rel': 'noopener', 'data-wpel-link': 'internal'})
        final_links = {}
        for i in links:
            url = f"https://api.shareus.io/v1/shorten?apiKey={api_key}&url={i['href']}"
            response = requests.get(url)
            link = response.json()
            final_links[f"{i.text}"] = link['shortenedUrl']
        movie_details["links"] = final_links
    return movie_details
