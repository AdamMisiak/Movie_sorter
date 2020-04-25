from movie_sorter.movie_sorter_oop import MovieSorter


def test_create_table():
	movie_sorter = MovieSorter()
	movies = movie_sorter.create_table()
	shape = movies.shape
	assert shape[0] == 100
	assert shape[1] == 23
	assert movies.loc[5, 'title'] == 'The Dark Knight'
	assert movies.loc[5, 'director'] == ['Christopher Nolan']
