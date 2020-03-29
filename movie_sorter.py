import pandas as pd
import requests
import sys

def creating_table():
	#READING CSV FILE
	movies = pd.read_csv("movies.csv")

	movies['genre'] = movies['genre'].astype('object')
	movies['director'] = movies['director'].astype('object')
	movies['cast'] = movies['cast'].astype('object')
	movies['writer'] = movies['writer'].astype('object')
	movies['language'] = movies['language'].astype('object')
	movies['country'] = movies['country'].astype('object')

	#ADDING/DELETING COLUMNS
	movies.insert(10, 'oscars_won', 0)
	movies.insert(11, 'oscars_nominated', 0)
	movies = movies.drop('awards', 1)

	#FILLING TABLE WITH DATA
	for index, title in enumerate(movies['title']):
		title = title.replace(' ', '+')
		full_url = 'http://www.omdbapi.com/?t=' + title + '&apikey=68ecd7ba'
		whole_movie_info = requests.get(full_url)
		whole_movie_info = whole_movie_info.json()

		movies.loc[index:index, 'year'] = whole_movie_info["Year"]
		movies.loc[index:index, 'runtime'] = whole_movie_info["Runtime"][:-3]
		movies.at[index, 'genre'] = whole_movie_info["Genre"].split(",")
		movies.at[index, 'director'] = whole_movie_info["Director"].split(",")
		movies.at[index, 'cast'] = whole_movie_info["Actors"].split(",")
		movies.at[index, 'writer'] = whole_movie_info["Writer"].split(",")
		movies.at[index, 'language'] = whole_movie_info["Language"].split(",")
		movies.at[index, 'country'] = whole_movie_info["Country"].split(",")

		awards_list_all = whole_movie_info["Awards"].split(' ')
		if awards_list_all[0] == 'Won' and 'Oscar' in awards_list_all[2]:
			movies.at[index, 'oscars_won'] = int(awards_list_all[1])
		else:
			movies.at[index, 'oscars_won'] = 0

		if awards_list_all[0] == 'Nominated' and 'Oscar' in awards_list_all[3]:
			movies.at[index, 'oscars_nominated'] = int(awards_list_all[2])
		else:
			movies.at[index, 'oscars_nominated'] = 0

		movies.loc[index:index, 'imdb_rating'] = float(whole_movie_info["imdbRating"])
		movies.loc[index:index, 'imdb_votes'] = whole_movie_info["imdbVotes"].replace(',', '')
		#movies.loc[index:index, 'box_office'] = whole_movie_info['BoxOffice']

	movies['imdb_votes'] = movies['imdb_votes'].astype(int)
	movies['runtime'] = movies['runtime'].astype(int)
	movies['year'] = movies['year'].astype(int)
	movies['oscars_won'] = movies['oscars_won'].astype(int)
	movies['oscars_nominated'] = movies['oscars_nominated'].astype(int)

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
	print(table[['title', sorting_by]].head(50))
	print(table[['title', 'oscars_won', 'oscars_nominated']])
	return table

def main():
	input_function = sys.argv[1]
	function_argument = sys.argv[2]
	if input_function == 'sort_by':
		if len(sys.argv) < 4:
			sorting_movies(function_argument, False)
		else:
			if sys.argv[3] == 'a':
				sorting_movies(function_argument, False)
			elif sys.argv[3] == 'd':
				sorting_movies(function_argument, True)

if(__name__ == "__main__"):
	main()


