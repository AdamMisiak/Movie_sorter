import pandas as pd
import requests

movies = pd.read_csv("movies.csv")
api = requests.get('http://www.omdbapi.com/?i=tt3896198&apikey=68ecd7ba')
api_json = api.json()

for title in movies['title']:
	title = title.replace(' ', '+')
	get_title = 'http://www.omdbapi.com/?t=' + title + '&apikey=68ecd7ba'
	all_movies_info = requests.get(get_title)
	all_movies_info = all_movies_info.json()
	movies['year'] = all_movies_info["Year"]
	print(movies)
	print(all_movies_info)
