import requests
import bs4

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from string import punctuation

import re
import json
import csv


# Fetching the Movie ids for top 5 movies
def movies_id_func():
    movies_ids = []
    try:
        request_res = requests.get("https://www.imdb.com/chart/top/")
        soup = bs4.BeautifulSoup(request_res.text, 'lxml')

        for i in range(5):
            movie_id = soup.select(".titleColumn")[i]('a')[0]['href'][7:-1]
            movies_ids.append(movie_id)
        return movies_ids
    except IndexError:
        print("Incorrect Index parsed")
    except requests.exceptions.ConnectionError:
        print("Connection Error, Check your Internet connectivity")
    except:
        print("Invalid URL")

ids = movies_id_func()

# Fetching the synposis for the above movies and storings

def movies_synopsis_func(movie_id):
    movies_synopsis = []

    for i in movie_id:
        request_movie_link = requests.get(f"https://www.imdb.com/title/{i}")
        if request_movie_link.status_code == 200:
            format_response = bs4.BeautifulSoup(request_movie_link.text, 'lxml')            
            movies_synopsis.append(format_response.select('.ipc-html-content')[1].getText())
        else:
            return "Incorrect URL"
    return movies_synopsis
synopsis = movies_synopsis_func(ids)

# creating a bag of words of synopsis and addin that in the dictionary with key as film_id

def bag_of_words(string):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(string)
    filtered_sentence = [word for word in word_tokens if not word.lower() in stop_words]
    bag_of_word = ' '.join(filtered_sentence)
    return bag_of_word

dictionary_movie_data = {}
i = 0
for string in synopsis:
    my_punctuation = punctuation.replace("'", "")
    new_str = string.translate(str.maketrans("", "", my_punctuation))
    dictionary_movie_data[ids[i]] = {"Synopsis" : bag_of_words(new_str)}
    i+=1


# api data fetching

def fetch_api_data(id):
    pattern = r"\D{2}\d{7}"
    if re.compile(pattern).match(id).group()==id:
        response = requests.get(f"http://www.omdbapi.com/?i={id}&apikey=1db04143")
        api_info = response.json()
        return api_info


for i in ids:
    api_call = fetch_api_data(i)
    dictionary_movie_data[i]['Genre'] = api_call['Genre']
    dictionary_movie_data[i]['Actors'] = api_call['Actors']


fields = ['movie_id', 'Synopsis', 'Genre', 'Actors']

with open("movies_data.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, fields)
    writer.writeheader()
    for key in dictionary_movie_data:
        writer.writerow({field: dictionary_movie_data[key].get(field) or key for field in fields})

