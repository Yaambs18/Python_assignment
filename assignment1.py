import requests
import bs4

request_res = requests.get("https://www.imdb.com/chart/top/")

soup = bs4.BeautifulSoup(request_res.text, 'lxml')

# Fetching the Movie ids for top 5 movies
movies_ids = []


for i in range(5):
    movie_id = soup.select(".titleColumn")[i]('a')[0]['href'][7:-1]
    movies_ids.append(movie_id)

# Fetching the synposis for the above movies and storings

movies_synopsis = []


for i in range(5):
    request_movie_link = requests.get(f"https://www.imdb.com/title/{movies_ids[i]}/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e31d89dd-322d-4646-8962-327b42fe94b1&pf_rd_r=SCCQEDQ3A70KXDN2HEMG&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_tt_{i+1}")
    
    format_response = bs4.BeautifulSoup(request_movie_link.text, 'lxml')
    
    movies_synopsis.append(format_response.select('.ipc-html-content')[1].getText())

print(movies_synopsis)