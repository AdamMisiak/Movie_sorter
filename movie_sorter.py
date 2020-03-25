import pandas as pd
import requests

movies = pd.read_csv("movies.csv")
api = requests.get('http://www.omdbapi.com/?i=tt3896198&apikey=68ecd7ba')
api_json = api.json()
g
for index, title in enumerate(movies['title']):

	title_raw = title
	title = title.replace(' ', '+')
	get_title = 'http://www.omdbapi.com/?t=' + title + '&apikey=68ecd7ba'
	all_movies_info = requests.get(get_title)
	all_movies_info = all_movies_info.json()
	movies.loc[index:index, 'year'] = all_movies_info["Year"]
	movies.loc[index:index, 'runtime'] = all_movies_info["Runtime"]
	movies.loc[index:index, 'genre'] = all_movies_info["Genre"]
	movies.loc[index:index, 'director'] = all_movies_info["Director"]
	movies.loc[index:index, 'cast'] = all_movies_info["Actors"]
	movies.loc[index:index, 'writer'] = all_movies_info["Runtime"]
	movies.loc[index:index, 'language'] = all_movies_info["Language"]
	movies.loc[index:index, 'country'] = all_movies_info["Country"]
	movies.loc[index:index, 'awards'] = all_movies_info["Awards"]
	movies.loc[index:index, 'imdb_rating'] = all_movies_info["imdbRating"]
	movies.loc[index:index, 'imdb_votes'] = all_movies_info["imdbVotes"]
	# movies.loc[index:index, 'box_office'] = all_movies_info['BoxOffice']
	print(movies)
	print(all_movies_info)
