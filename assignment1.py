import requests
import bs4
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from string import punctuation
import re
import csv
import os
import logging

logging.basicConfig(filename="assignment_file.log", format='%(asctime)s %(message)s', filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

# Fetching the Movie ids for top 5 movies
base_url = "https://www.imdb.com/chart/top/"

movies_ids = []
movies_synopsis = []
dictionary_movie_data = {}

def movies_id_func(url):
    
    try:
        request_res = requests.get(url)
        soup = bs4.BeautifulSoup(request_res.text, 'lxml')

        for i in range(5):
            movie_id = soup.select(".titleColumn")[i]('a')[0]['href'][7:-1]
            movies_ids.append(movie_id)
        return movies_ids
    except requests.exceptions.ConnectionError:
        logging.error("Connection Error, Check your Internet connectivity")
    except requests.exceptions.MissingSchema:
        logging.error("Invalid URL")
        
# Fetching the synposis for the above movies and storings

def movies_synopsis_func(movie_id):
    try:
        for i in movie_id:
            request_movie_link = requests.get(f"https://www.imdb.com/title/{i}")
            if request_movie_link.status_code == 200:
                format_response = bs4.BeautifulSoup(request_movie_link.text, 'lxml')            
                movies_synopsis.append(format_response.select('.ipc-html-content')[1].getText())
            else:
                logging.info("Incorrect URL")
        return movies_synopsis
    except TypeError:
        logging.error("None object returned")

# creating a bag of words of synopsis and addin that in the dictionary with key as film_id

def bag_of_words(string):
    try:
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(string)
        filtered_sentence = [word for word in word_tokens if not word.lower() in stop_words]
        bag_of_word = ' '.join(filtered_sentence)
        return bag_of_word
    except TypeError:
        logging.error("Missing argument")

# api data fetching

def fetch_api_data(movie_ids):
    try:
        for id in movie_ids:
            pattern = r"\D{2}\d{7}"
            if re.compile(pattern).match(id).group()==id:
                response = requests.get(f"http://www.omdbapi.com/?i={id}&apikey=1db04143")
                api_info = response.json()
            try:
                dictionary_movie_data[id]['Genre'] = api_info['Genre']
                dictionary_movie_data[id]['Actors'] = api_info['Actors']
                dictionary_movie_data[id]['Title'] = api_info['Title']
            except KeyError:
                logging.error("json file returned None")
    except TypeError:
            logging.error("Missing arguments or Unexpected argument")
    return dictionary_movie_data

fields = ['movie_id','Title', 'Synopsis', 'Genre', 'Actors']
# csv file creation

def write_csv():
    if os.path.exists('movies_data.csv'):
        csvfile = open("movies_data.csv", "r")
        reader = csv.DictReader(csvfile)
        for row in reader:
            for item in movies_ids:
                if row['movie_id']==item:
                    dictionary_movie_data.pop(item)

        csvfile.close()
        if len(dictionary_movie_data)>0:
            with open("movies_data.csv", "a") as file:
                writer = csv.DictWriter(file, fields)
                for key in dictionary_movie_data:
                    writer.writerow({field: dictionary_movie_data[key].get(field) or key for field in fields})
            
    else:
        with open("movies_data.csv", "w") as csvfile:
            writer = csv.DictWriter(csvfile, fields)
            writer.writeheader()
            for key in dictionary_movie_data:
                writer.writerow({field: dictionary_movie_data[key].get(field) or key for field in fields})


def fetch_movies_data():
    
    item = input("Enter Genre or Actor name for data fetching: ")
    if item and not item.isdigit():
        with open("movies_data.csv", 'r') as file:
            reader = csv.DictReader(file)
            movie_names = []
            for row in reader:
                if item in row['Actors'] or item in row['Genre']:
                    movie_names.append(row['Title'])
            return movie_names


if __name__ == "__main__":
    logging.info(movies_id_func(base_url))
    logging.info(movies_synopsis_func(movies_ids))
    i = 0
    for string in movies_synopsis:
        my_punctuation = punctuation.replace("'", "")
        new_str = string.translate(str.maketrans("", "", my_punctuation))
        dictionary_movie_data[movies_ids[i]] = {"Synopsis" : bag_of_words(new_str)}
        i+=1

    logging.info(fetch_api_data(movies_ids))
    write_csv()
    fetched_data = fetch_movies_data()
    print(fetched_data)
    logging.info(fetched_data)