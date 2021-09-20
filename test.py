from assignment1 import fetch_api_data
import csv
def fetch_movies_data():
    item = input("Enter Genre or Actor name for data fetching: ")
    with open("movies_data.csv", 'r') as file:
        reader = csv.DictReader(file)
        rows = [row for row in reader if row['Actors']==item or row['Genre']==item]
        return rows

print(fetch_movies_data())