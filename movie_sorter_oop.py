import pandas as pd
import numpy as np
import requests
import sys


class MovieSorter:

	def create_table(self):
		# READING CSV FILE
		movies = pd.read_csv("movies.csv")

		movies['genre'] = movies['genre'].astype('object')
		movies['director'] = movies['director'].astype('object')
		movies['cast'] = movies['cast'].astype('object')
		movies['writer'] = movies['writer'].astype('object')
		movies['language'] = movies['language'].astype('object')
		movies['country'] = movies['country'].astype('object')

		# ADDING/DELETING COLUMNS
		movies.insert(10, 'oscars_won', 0)
		movies.insert(11, 'oscars_nominated', 0)
		movies.insert(12, 'globes_won', 0)
		movies.insert(13, 'globes_nominated', 0)
		movies.insert(14, 'bafta_won', 0)
		movies.insert(15, 'bafta_nominated', 0)
		movies.insert(16, 'another_won', 0)
		movies.insert(17, 'another_nominated', 0)
		movies.insert(18, 'all_won', 0)
		movies.insert(19, 'all_nominated', 0)
		movies = movies.drop('awards', 1)

		# FILLING TABLE WITH DATA
		for index, title in enumerate(movies['title']):

			# GETTING API KEY + DATA
			title = title.replace(' ', '+')
			full_url = 'http://www.omdbapi.com/?t=' + title + '&apikey=68ecd7ba'
			whole_movie_info = requests.get(full_url)
			whole_movie_info = whole_movie_info.json()

			movies.loc[index:index, 'year'] = whole_movie_info["Year"]
			movies.loc[index:index, 'runtime'] = whole_movie_info["Runtime"][:-3]
			movies.at[index, 'genre'] = whole_movie_info["Genre"].replace(' ', '').split(",")
			movies.at[index, 'director'] = whole_movie_info["Director"].split(", ")
			movies.at[index, 'cast'] = whole_movie_info["Actors"].split(", ")
			movies.at[index, 'writer'] = whole_movie_info["Writer"].split(", ")
			movies.at[index, 'language'] = whole_movie_info["Language"].replace(' ', '').split(",")
			movies.at[index, 'country'] = whole_movie_info["Country"].replace(' ', '').split(",")

			# CREATING AWARDS COLUMNS
			awards_list_all = whole_movie_info["Awards"].split(' ')
			if awards_list_all[0] == 'Won' and 'Oscar' in awards_list_all[2]:
				movies.at[index, 'oscars_won'] = int(awards_list_all[1])
			else:
				movies.at[index, 'oscars_won'] = 0

			if awards_list_all[0] == 'Nominated' and 'Oscar' in awards_list_all[3]:
				movies.at[index, 'oscars_nominated'] = int(awards_list_all[2])
			else:
				movies.at[index, 'oscars_nominated'] = 0

			if awards_list_all[0] == 'Won' and 'Globe' in awards_list_all[2]:
				movies.at[index, 'globes_won'] = int(awards_list_all[1])
			else:
				movies.at[index, 'globes_won'] = 0

			if awards_list_all[0] == 'Nominated' and 'Globe' in awards_list_all[4]:
				movies.at[index, 'globes_nominated'] = int(awards_list_all[2])
			else:
				movies.at[index, 'globes_nominated'] = 0

			if awards_list_all[0] == 'Won' and 'BAFTA' in awards_list_all[2]:
				movies.at[index, 'bafta_won'] = int(awards_list_all[1])
			else:
				movies.at[index, 'bafta_won'] = 0

			if awards_list_all[0] == 'Nominated' and 'BAFTA' in awards_list_all[3]:
				movies.at[index, 'bafta_nominated'] = int(awards_list_all[2])
			else:
				movies.at[index, 'bafta_nominated'] = 0

			if 'wins' in awards_list_all:
				index_of_win = awards_list_all.index('wins')
				movies.at[index, 'another_won'] = int(awards_list_all[index_of_win - 1])
			elif 'wins.' in awards_list_all:
				index_of_win = awards_list_all.index('wins.')
				movies.at[index, 'another_won'] = int(awards_list_all[index_of_win - 1])
			else:
				index_of_win = 0
				movies.at[index, 'another_won'] = 0

			if 'nominations' in awards_list_all:
				index_of_nominations = awards_list_all.index('nominations')
				movies.at[index, 'another_nominated'] = int(awards_list_all[index_of_nominations - 1])
			elif 'nominations.' in awards_list_all:
				index_of_nominations = awards_list_all.index('nominations.')
				movies.at[index, 'another_nominated'] = int(awards_list_all[index_of_nominations - 1])
			else:
				index_of_nominations = 0
				movies.at[index, 'another_nominated'] = 0

			# CALCULATING TOTAL NUMBER OF WINS AND NOMINATIONS
			movies.loc[index:index, 'all_won'] = movies.iloc[index]['oscars_won'] + movies.iloc[index]['globes_won'] + \
												 movies.iloc[index]['bafta_won'] + movies.iloc[index]['another_won']

			movies.loc[index:index, 'all_nominated'] = movies.iloc[index]['oscars_nominated'] + \
													   movies.iloc[index]['globes_nominated'] + \
													   movies.iloc[index]['bafta_nominated'] + \
													   movies.iloc[index]['another_nominated']

			movies.loc[index:index, 'imdb_rating'] = float(whole_movie_info["imdbRating"])
			movies.loc[index:index, 'imdb_votes'] = whole_movie_info["imdbVotes"].replace(',', '')

			box_office_movies = str(whole_movie_info.get('BoxOffice'))
			if box_office_movies == "N/A" or box_office_movies == "None":
				box_office_movies = 0
			else:
				box_office_movies = box_office_movies[1:].replace(',', '')
			movies.loc[index:index, 'box_office'] = box_office_movies

		# CHANGING TYPES OF COLUMNS
		movies['year'] = movies['year'].astype(int)
		movies['runtime'] = movies['runtime'].astype(int)
		movies['oscars_won'] = movies['oscars_won'].astype(int)
		movies['oscars_nominated'] = movies['oscars_nominated'].astype(int)
		movies['imdb_votes'] = movies['imdb_votes'].astype(int)
		movies['box_office'] = movies['box_office'].astype(int)

		print('First ten rows of full table:')
		# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
		# 	print(movies)
		print(movies.head(10))
		movies.to_csv('movies_filled.csv', index=False)
		return movies

	def sorting_movies(self, table_filled, sorting_by, descending):
		if descending:
			print('Sorting movies by:', sorting_by, 'descending...')
		else:
			print('Sorting movies by:', sorting_by, 'ascending...')
		try:
			table = pd.read_csv(table_filled)
		except:
			table = self.create_table()
		if descending:
			table.sort_values(by=sorting_by, inplace=True, ascending=False)
		else:
			table.sort_values(by=sorting_by, inplace=True)
		sorting_by.append('title')

		#print(table[sorting_by])
		return table

	def filtering_movies(self, table_filled, column, filtering_by):
		print('Filtering movies by:', filtering_by, 'in', column, 'column...')
		try:
			table = pd.read_csv(table_filled)
		except:
			table = self.create_table()
		if table[column].dtype == np.int64:
			filtering_by = int(filtering_by)
			table = table[table[column] == filtering_by]
			print(table[['title', column]])
		elif table[column].dtype == np.float64:
			filtering_by = float(filtering_by)
			table = table[table[column] == filtering_by]
			print(table[['title', column]])
		elif table[column].dtype == np.object:
			index_list = []
			for index, row in table.iterrows():
				if filtering_by in row[column]:
					index_list.append(index)
			table = table.loc[index_list]
			print(table.loc[index_list, ['title', column]])
		return table

	def oscars_nominated_but_no_won(self, table_filled):
		print('Filtering movies that were nominated for Oscar but did not win any')
		try:
			table = pd.read_csv(table_filled)
		except:
			table = self.create_table()
		table = table[table['oscars_nominated'] > 0]
		table = table[table['oscars_won'] == 0]
		print(table[['title', 'oscars_nominated', 'oscars_won']])
		return table

	def won_80_of_nominations(self, table_filled):
		print('Filtering movies that won more than 80% of nominations...')
		try:
			table = pd.read_csv(table_filled)
		except:
			table = self.create_table()
		table.insert(20, 'won_to_nominated', 0)
		for index, title in enumerate(table['title']):
			all_won = table.at[index, 'all_won']
			if table.at[index, 'all_nominated'] != 0:
				all_nominated = table.at[index, 'all_nominated']
				table.at[index, 'won_to_nominated'] = float((all_won / all_nominated) * 100)
		table = table[table['won_to_nominated'] > 80]
		print(table[['title', 'all_won', 'all_nominated', 'won_to_nominated']])
		return table

	def box_office_100m(self, table_filled):
		print('Filtering movies that earned more than 100,000,000 $...')
		try:
			table = pd.read_csv(table_filled)
		except:
			table = self.create_table()
		table = table[table['box_office'] > 100000000]
		print(table[['title', 'box_office']])
		return table

	def comparing_movies(self, table_filled, column, movie1, movie2):
		print('Comparing movies:', movie1, 'and', movie2, 'by', column, '...')
		try:
			table = pd.read_csv(table_filled)
		except:
			table = self.create_table()
		table = table[['title', column]]
		cond1 = table[table['title'] == movie1]
		cond2 = table[table['title'] == movie2]
		table = cond1.append(cond2)
		print(table)
		return table

	def add_movie(self, table_filled, name):
		print('Adding movie:', name, 'to movies table...')
		try:
			table = pd.read_csv(table_filled)
		except:
			table = self.create_table()
		table = table.append({'title': name}, ignore_index=True)
		print(table.tail(10))
		return table

	def highscores_movies(self, table_filled):
		print('Creating table of highscores...')
		try:
			table = pd.read_csv(table_filled)
		except:
			table = self.create_table()
		table_columns = ['runtime', 'oscars_won', 'oscars_nominated', 'globes_nominated', 'bafta_nominated', 'another_won',
						 'another_nominated', 'all_won', 'all_nominated', 'imdb_rating', 'imdb_votes', 'box_office']

		all_highscores_table = pd.DataFrame(columns=['Column', 'Movie', 'Value'])
		all_highscores_table['Column'] = table_columns
		for index, row in enumerate(table_columns):
			highscore_table = movie_sorter.sorting_movies('movies_filled.csv', [row], True)
			highscore_value = highscore_table[row].to_list()[0]
			highscore_movie = highscore_table['title'].to_list()[0]
			all_highscores_table.at[index, 'Value'] = highscore_value
			all_highscores_table.at[index, 'Movie'] = highscore_movie
		print(all_highscores_table)



movie_sorter = MovieSorter()
# table = movie_sorter.create_table()
movie_sorter.highscores_movies('movies_filled.csv')
# movie_sorter.sorting_movies('movies_filled.csv', ['oscars_won'], True)