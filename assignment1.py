import requests
import bs4

request_res = requests.get("https://www.imdb.com/chart/top/")

soup = bs4.BeautifulSoup(request_res.text, 'lxml')

# Fetching the Movie ids for top 5 movies
movies_ids = []


for i in range(5):
    movie_id = soup.select(".titleColumn")[i]('a')[0]['href'][7:-2]
    movies_ids.append(movie_id)





