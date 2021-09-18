import requests
import bs4

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from string import punctuation

import re
import json

request_res = requests.get("https://www.imdb.com/chart/top/")

soup = bs4.BeautifulSoup(request_res.text, 'lxml')

# Fetching the Movie ids for top 5 movies
def movies_id_func():
    movies_ids = []


    for i in range(5):
        movie_id = soup.select(".titleColumn")[i]('a')[0]['href'][7:-1]
        movies_ids.append(movie_id)

    return movies_ids

ids = movies_id_func()

# Fetching the synposis for the above movies and storings

def movies_synopsis_func(movie_id):
    movies_synopsis = []

    j = 1
    for i in movie_id:
        request_movie_link = requests.get(f"https://www.imdb.com/title/{i}/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e31d89dd-322d-4646-8962-327b42fe94b1&pf_rd_r=SCCQEDQ3A70KXDN2HEMG&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_tt_{j}")
        if request_movie_link.status_code == 200:
            j += 1
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
 
    filtered_sentence = []
    for i in word_tokens:
        if i not in stop_words:
            filtered_sentence.append(i)

    return filtered_sentence

dictionary_movie_data = {}
i = 0
for string in synopsis:
    my_punctuation = punctuation.replace("'", "")
    new_str = string.translate(str.maketrans("", "", my_punctuation))
    dictionary_movie_data[ids[i]] = bag_of_words(new_str)
    i+=1


# api data fetching

def fetch_api_data(id):
    pattern = r"\D{2}\d{7}"
    if re.compile(pattern).match(id).group()==id:
        response = requests.get(f"http://www.omdbapi.com/?i={id}&apikey=1db04143")
        api_info = response.json()
        return api_info
    
for i in ids:
    fetch_api_data(i)

