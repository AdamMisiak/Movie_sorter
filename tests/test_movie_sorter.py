from movie_sorter.movie_sorter import MovieSorter


def test_creating_table():
	movie_sorter = MovieSorter()
	movies = movie_sorter.creating_table()
	shape = movies.shape
	assert shape[0] == 100
	assert shape[1] == 23
	assert movies.loc[5, 'title'] == 'The Dark Knight'
	assert movies.loc[5, 'director'] == ['Christopher Nolan']
	assert movies.loc[5, 'imdb_rating'] == 9.0
	assert movies.loc[5, 'box_office'] == 533316061

def test_checking_table():
	movie_sorter = MovieSorter()
	movies = movie_sorter.checking_table('movies_filled.csv')
	shape = movies.shape
	assert shape[0] == 100
	assert shape[1] == 23
	assert movies.loc[99, 'title'] == 'The Big Lebowski'
	assert movies.loc[99, 'imdb_votes'] == 697372


def test_sorting_movies_one_column():
	movie_sorter = MovieSorter()
	movies = movie_sorter.sorting_movies('runtime', False)
	shape = movies.shape
	assert shape[0] == 100
	assert shape[1] == 3
	assert movies.loc[0, 'title'] == 'Shazam'
	assert movies.loc[0, 'runtime'] == 6


def test_sorting_movies_few_column():
	movie_sorter = MovieSorter()
	movies = movie_sorter.sorting_movies('imdb_rating,runtime', False)
	shape = movies.shape
	assert shape[0] == 100
	assert shape[1] == 4
	assert movies.loc[0, 'title'] == 'Ben Hur'
	assert movies.loc[0, 'runtime'] == 180
	assert movies.loc[0, 'imdb_rating'] == 6.3


def test_filtering_movies():
	movie_sorter = MovieSorter()
	movies = movie_sorter.filtering_movies('imdb_rating', 8.9)
	shape = movies.shape
	assert shape[0] == 2
	assert shape[1] == 3
	assert movies.loc[0, 'title'] == '12 Angry Men'
	assert movies.loc[0, 'imdb_rating'] == 8.9

