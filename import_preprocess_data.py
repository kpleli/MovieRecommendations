import pandas as pd
import numpy as np

def import_genre_information(cwd):
	#reads in u.genre, preprossces it and returns the pandas dataframe genre_information
	header = ['genre','genre_id']
	genre_information = pd.read_csv('u.genre', sep = '|', names = header)
	return genre_information
	
def import_movie_information(cwd,genre_information):
	#reads in u.item, preprossces it with headers from genre_information and returns the pandas dataframe movie_information
	header = ['movie_id','movie_title','release_date','blank','imbd_link']
	for genre in genre_information['genre']:
		header.append(genre)
	movie_information = pd.read_csv('u.item', sep = '|', names = header)
	movie_information = movie_information.drop(['release_date','blank','imbd_link'],axis = 1)
	return movie_information
	
def import_user_information(cwd):
	#reads in u.data, preprossces it, and returns the pandas dataframe user_information
	header = ['user_id','movie_id','movie_rating','timestamp']
	user_information = pd.read_csv('u.data', sep = '\t', names = header)
	user_information = user_information.drop(['timestamp'],axis = 1)
	return user_information

def merge_user_movie(user_information,movie_information):
	#creates a new data frame user_movie_merge which is the user_information and movie_information data frames matched on movie_id
	user_movie_merge = pd.merge(user_information, movie_information,left_on='movie_id',right_on="movie_id")
	return user_movie_merge
	
def create_rating_user_matrix(user_information):
	#creates and returns a matrix with the index being movie_id, columns being user_id and the value being movie_rating
	rating_user_matrix = user_information.pivot_table(index=['movie_id'],columns= ['user_id'],values = 'movie_rating')
	rating_user_matrix.reset_index(drop=True)
	rating_user_matrix.fillna(0,inplace = True)
	return rating_user_matrix.as_matrix()
	
def create_user_rating_matrix(user_information):
	#creates and returns a matrix with the index being user_id, columns being movie_id and the value being movie_rating
	user_ratings_matrix = user_information.pivot_table(index=['user_id'],columns= ['movie_id'],values = 'movie_rating')
	user_ratings_matrix.reset_index(drop=True)
	user_ratings_matrix.fillna(0,inplace = True)
	return user_ratings_matrix.as_matrix()
	