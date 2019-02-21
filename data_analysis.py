import pandas as pd

def highest_rated_movies(user_movie_merge,movie_information,k):
    #returns the movies with the highest average ratings, must have a minimum of 10 ratings
	groupby_movie = user_movie_merge.groupby('movie_id').mean()
	groupby_movie = groupby_movie.sort_values(by=['movie_rating'], ascending = False)
	groupby_movie = groupby_movie.reset_index()
	top_rated_movies = groupby_movie.iloc[0:groupby_movie.shape[0],[0,2]]
	movie_id_list = []
	avg_ratings = []
	for x in top_rated_movies['movie_id']:
		movie_id_list.append(x)
	for y in top_rated_movies['movie_rating']:
		avg_ratings.append(y)
	groupby_movie_count = user_movie_merge.groupby(['movie_id']).count()
	groupby_movie_count = groupby_movie_count.reset_index()
	i = 0
	count = 0
	print 'The top {} highest rated movies\n'.format(k)
	while (count < k):
		num_ratings = groupby_movie_count.loc[groupby_movie_count['movie_id'] == movie_id_list[i]]
		num_ratings = num_ratings.iloc[0,2]
		if num_ratings <= 10:
			i += 1
			pass
		else:
			title = get_movie_title(movie_information,movie_id_list[i])
			avg_rating = avg_ratings[i]
			print '{}, Number of Ratings: {}, Average Rating {:0.2f}'.format(title,num_ratings,avg_rating)
			i += 1
			count += 1

def most_rated_movies_by_number(user_movie_merge,movie_information,k):
	#returns the movies that were rated most frequent along with their frequency count and average rating, regardless of their average rating
    groupby_movie = user_movie_merge.groupby('movie_id').count()
    groupby_movie = groupby_movie.sort_values(by=['user_id'], ascending = False)
    groupby_movie = groupby_movie.reset_index()
    top_rated_movies = groupby_movie.iloc[0:k,0:2]
    movie_id_list = []
    count_list = []
    for x in top_rated_movies['movie_id']:
        movie_id_list.append(x)
    for y in top_rated_movies['user_id']:
        count_list.append(y)
    groupby_movie_average = user_movie_merge.groupby('movie_id').mean()
    groupby_movie_average = groupby_movie_average.reset_index()
    avg_ratings = []
    for z in movie_id_list:
        xx = groupby_movie_average.loc[groupby_movie_average['movie_id'] == z]
        xxx = xx.iloc[0,2]
        avg_ratings.append(xxx)
    print 'The top {} rated movies by number of ratings\n'.format(k)
    for i in range(k):
        title = get_movie_title(movie_information,movie_id_list[i])
        num_ratings = count_list[i]
        avg_rating = avg_ratings[i]
        print '{}, Number of Ratings: {}, Average Rating {:0.2f}'.format(title,num_ratings,avg_rating)
		
		
def highest_rated_movies_by_genre(user_movie_merge,movie_information,genre,k):
    #groups and returns the highest average ratings of movies by genre, must have a minimum of 10 ratings
	groupby_genre = user_movie_merge.groupby(['movie_id',genre]).mean()
	groupby_genre = groupby_genre.sort_values(by=['movie_rating'], ascending = False)
	groupby_genre = groupby_genre.reset_index()
	groupby_genre = groupby_genre.loc[groupby_genre[genre] == 1]
	top_rated_movies = groupby_genre.iloc[0:groupby_genre.shape[0],[0,3]]
	movie_id_list = []
	avg_ratings = []
	for x in top_rated_movies['movie_id']:
		movie_id_list.append(x)
	for y in top_rated_movies['movie_rating']:
		avg_ratings.append(y)
	groupby_genre_count = user_movie_merge.groupby(['movie_id',genre]).count()
	groupby_genre_count = groupby_genre_count.reset_index()
    
	groupby_genre_count = groupby_genre_count.loc[groupby_genre_count[genre] == 1]
	i = 0
	count = 0
	print 'The top {} highest rated movies in {} genre\n'.format(k, genre)
	while (count < k):
        
		num_ratings = groupby_genre_count.loc[groupby_genre_count['movie_id'] == movie_id_list[i]]
		num_ratings = num_ratings.iloc[0,2]
        
		if num_ratings <= 10:
			i += 1
			pass
		else:
			title = get_movie_title(movie_information,movie_id_list[i])
			avg_rating = avg_ratings[i]
			print '{}, Number of Ratings: {}, Average Rating {:0.2f}'.format(title,num_ratings,avg_rating)
			i += 1
			count += 1
			
def get_movie_title(movie_information,movie_id):
	#return movie_title based on movie_id inputted
    movie_row = movie_information.loc[movie_information['movie_id'] == movie_id]
    movie_title = movie_row.iloc[0,1]
    return movie_title