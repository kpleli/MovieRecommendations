import pandas as pd
import numpy as np
from sklearn.metrics import pairwise_distances
from numpy import linalg as la
from numpy import *

def recommendations_based_on_item(rating_user_matrix,movie_information,movie_title,num_recommendations):
    #input movie title and find similiarity to other movies. output specified number of recommendations
	distances = pairwise_distances(rating_user_matrix, metric = 'cosine')
	similiarities = 1-distances
	np.fill_diagonal(similiarities, 0) 
	movie_id = get_movieid(movie_information,movie_title)
	similiarities_df = pd.DataFrame(similiarities)
	similiarities_df.index = range(1,movie_information.shape[0]+1)
    
	movie_sim_row = similiarities_df.iloc[movie_id-1]
	movie_information['Similiarity']= movie_sim_row
	movie_information_sorted = movie_information.sort_values(['Similiarity'],ascending = False)
	movies = movie_information_sorted.iloc[0:num_recommendations,0:2]
	print 'Top {} Recommendations based on input of {}:\n'.format(num_recommendations,movie_title)
	for x in movies['movie_title']:
		print x
		
def get_movieid(movie_information,movie_title):
	#given movie_title return movie_id
    movie_row = movie_information.loc[movie_information['movie_title']==movie_title]
    movie_id = movie_row.iloc[0,0]
    return movie_id
	
def cosine_similiarity(userA,userB):
	#function to calculate cosine similiarirty between 2 users
    num = float(userA.T * userB)
    denom = la.norm(userA)*la.norm(userB)
    return 0.5 + 0.5 * (num / denom)

def standard_estimate(user_rating_matrix, user, simMeas, item):
	#predict and return user rating of non-rated movies 
    n = shape(user_rating_matrix)[1]
    simTotal = 0.0; ratSimTotal = 0.0
    for j in range(n):
        userRating = user_rating_matrix[user,j]
        if userRating == 0: continue
        overLap = nonzero(logical_and(user_rating_matrix[:,item]>0, \
                                      user_rating_matrix[:,j]>0))[0]
        if len(overLap) == 0: similarity = 0
        else: similarity = simMeas(user_rating_matrix[overLap,item], \
                                   user_rating_matrix[overLap,j])
        simTotal += similarity
        ratSimTotal += similarity * userRating
    if simTotal == 0: return 0
    else: return ratSimTotal/simTotal

def get_movie_title(movie_information,movie_id):
    #given movie_id return movie title
	movie_row = movie_information.loc[movie_information['movie_id'] == movie_id]
	movie_title = movie_row.iloc[0,1]
	return movie_title

def recommend_movies(user_rating_matrix, user, num_recommendations, simMeas=cosine_similiarity, estMethod=standard_estimate):
    #calls standard_estimate function to get predicited ratings of non-rated items returns list of movie_ids and predicted ratings in descending order
	unratedItems = np.nonzero(user_rating_matrix[user,:].A==0)[1]
	if len(unratedItems) == 0: return 'you rated everything'
	itemScores = []
	for item in unratedItems:
		estimatedScore = estMethod(user_rating_matrix, user, simMeas, item)
		itemScores.append((item, estimatedScore))
	return sorted(itemScores, key=lambda jj: jj[1], reverse=True)[:num_recommendations]
	
def print_recommendations_based_on_ratings(user_rating_matrix,movie_information,user_id,num_recommendations):
    #call recommend_movie and output specified number of recommended movie titles
	recommendations = recommend_movies(user_rating_matrix,user_id,num_recommendations)
	movie_list = []
	print 'Top {} Movie Recommendations Based on Your Ratings\n'.format(num_recommendations)
	for n in range(num_recommendations):
		movie_id = recommendations[n][0]
		movie_title = get_movie_title(movie_information,movie_id)
		print movie_title