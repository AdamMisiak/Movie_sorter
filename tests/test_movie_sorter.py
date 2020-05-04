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


def test_oscars_nominated_but_no_won():
	movie_sorter = MovieSorter()
	movies = movie_sorter.oscars_nominated_but_no_won()
	shape = movies.shape
	assert shape[0] == 30
	assert shape[1] == 4
	assert movies.loc[0, 'title'] == 'The Shawshank Redemption'
	assert movies.loc[0, 'oscars_nominated'] == 7
	assert movies.loc[0, 'oscars_won'] == 0
	assert movies.loc[29, 'title'] == 'Blade Runner'
	assert movies.loc[29, 'oscars_nominated'] == 2
	assert movies.loc[29, 'oscars_won'] == 0


def test_won_to_nominated():
	movie_sorter = MovieSorter()
	movies = movie_sorter.won_80_of_nominations()
	shape = movies.shape
	assert shape[0] == 44
	assert shape[1] == 5
	assert movies.loc[0, 'title'] == 'Memento'
	assert movies.loc[0, 'all_won'] == 57
	assert movies.loc[0, 'all_nominated'] == 58
	assert movies.loc[0, 'won_to_nominated'] == 98
	assert movies.loc[43, 'title'] == 'Gran Torino'
	assert movies.loc[43, 'all_won'] == 21
	assert movies.loc[43, 'all_nominated'] == 21
	assert movies.loc[43, 'won_to_nominated'] == 100


def test_box_office_100m():
	movie_sorter = MovieSorter()
	movies = movie_sorter.box_office_100m()
	shape = movies.shape
	assert shape[0] == 13
	assert shape[1] == 3
	assert movies.loc[0, 'title'] == 'The Dark Knight'
	assert movies.loc[0, 'box_office'] == 533316061


def test_comparing_movies():
	movie_sorter = MovieSorter()
	movies = movie_sorter.comparing_movies('imdb_rating', 'Warrior', 'Coco')
	shape = movies.shape
	assert shape[0] == 2
	assert shape[1] == 3
	assert movies.loc[0, 'title'] == 'Warrior'
	assert movies.loc[0, 'imdb_rating'] == 8.2


def test_adding_movie():
	movie_sorter = MovieSorter()
	movies_before = movie_sorter.creating_table()
	shape_before = movies_before.shape
	movies_after = movie_sorter.adding_movie('Harry Potter')
	shape_after = movies_after.shape
	assert shape_before[0] == 100
	assert shape_after[0] == 101
	assert shape_after[1] == 23
	assert movies_after.loc[0, 'title'] == 'The Shawshank Redemption'
	assert movies_after.loc[100, 'title'] == 'Harry Potter'


def test_highscores_movies():
	movie_sorter = MovieSorter()
	movies = movie_sorter.highscores_movies()
	shape = movies.shape
	assert shape[0] == 12
	assert shape[1] == 3
	assert movies.loc[0, 'Column'] == 'runtime'
	assert movies.loc[0, 'Movie'] == 'Gone with the Wind'
	assert movies.loc[0, 'Value'] == 238

