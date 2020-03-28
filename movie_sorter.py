import pandas as pd
import requests
import sys

def creating_table():
	movies = pd.read_csv("movies.csv")
	for index, title in enumerate(movies['title']):
		title = title.replace(' ', '+')
		full_url = 'http://www.omdbapi.com/?t=' + title + '&apikey=68ecd7ba'
		whole_movie_info = requests.get(full_url)
		whole_movie_info = whole_movie_info.json()
		movies.loc[index:index, 'year'] = whole_movie_info["Year"]
		movies.loc[index:index, 'runtime'] = whole_movie_info["Runtime"][:-3]
		movies.loc[index:index, 'genre'] = whole_movie_info["Genre"]
		# print(type(whole_movie_info["Genre"]))
		# print(whole_movie_info["Genre"].split(","))
		# print(type(whole_movie_info["Genre"].split(",")))
		movies.loc[index:index, 'director'] = whole_movie_info["Director"]
		movies.loc[index:index, 'cast'] = whole_movie_info["Actors"]
		movies.loc[index:index, 'writer'] = whole_movie_info["Writer"]
		movies.loc[index:index, 'language'] = whole_movie_info["Language"]
		movies.loc[index:index, 'country'] = whole_movie_info["Country"]
		movies.loc[index:index, 'awards'] = whole_movie_info["Awards"]
		movies.loc[index:index, 'imdb_rating'] = float(whole_movie_info["imdbRating"])
		movies.loc[index:index, 'imdb_votes'] = whole_movie_info["imdbVotes"].replace(',', '')
		#movies.loc[index:index, 'box_office'] = whole_movie_info['BoxOffice']

	movies['imdb_votes'] = movies['imdb_votes'].astype(int)
	movies['runtime'] = movies['runtime'].astype(int)
	movies['year'] = movies['year'].astype(int)

	with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
		print(movies)
	return movies

def sorting_movies(sorting_by, descending):
	table = creating_table()
	if descending:
		table.sort_values(by=[sorting_by], inplace=True, ascending=False)
	else:
		table.sort_values(by=[sorting_by], inplace=True)
	print(table)
	return table

def main():
	input_function = sys.argv[1]
	function_argument = sys.argv[2]
	if input_function == 'sorting_by':
		if len(sys.argv) < 4:
			sorting_movies(function_argument, False)
		else:
			if sys.argv[3] == 'a':
				sorting_movies(function_argument, False)
			elif sys.argv[3] == 'd':
				sorting_movies(function_argument, True)

if(__name__ == "__main__"):
	main()