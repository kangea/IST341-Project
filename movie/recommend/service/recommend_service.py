import pandas as pd 
import turicreate as tc
import os
from sklearn.model_selection import train_test_split

file_link = "links.csv"
file_movies_ratings = "movies_ratings.csv"
file_movies = "movies.csv"
file_ratings = "ratings.csv"
file_tags = "tags.csv"

dir_loc = os.path.dirname(os.path.realpath(__file__))+'/../../../data/'
#link_sf = tc.SFrame.read_csv('+file_link)

movies_ratings = pd.read_csv(dir_loc+file_movies_ratings)
movies = pd.read_csv(dir_loc+file_movies)
link = pd.read_csv(dir_loc+file_link)

user_id = "userId"
item_id = "movieId"
target = "rating"

def split_data(data):
    '''
    Splits dataset into training and test set.
    
    Args:
        data (pandas.DataFrame)
        
    Returns
        train_data (tc.SFrame)
        test_data (tc.SFrame)
    '''
    train, test = train_test_split(data, test_size = .2)
    train_data = tc.SFrame(train)
    test_data = tc.SFrame(test)
    return train_data, test_data


train_data, test_data = split_data(movies_ratings)

def model_popular(train_data, user_id, item_id, target):
  return tc.popularity_recommender.create(train_data,user_id=user_id,item_id=item_id,target=target)

def model_cosine(train_data, user_id, item_id, target):
  return tc.item_similarity_recommender.create(train_data,user_id=user_id,item_id=item_id,target=target, similarity_type='cosine')

def model_pearson(train_data, user_id, item_id, target):
  return tc.item_similarity_recommender.create(train_data,user_id=user_id,item_id=item_id,target=target, similarity_type='pearson')

def recommend_model(model, users, rec_size):
  recommand = model.recommend(users=users, k=rec_size)
  #recommand.print_rows(display_size)
  return recommand

def test_modeling():
  users = [135,136,137]
  model_po = model_popular(train_data, user_id, item_id, target)
  recommend_model(model_po, users, 5)

  model_c = model_cosine(train_data, user_id, item_id, target)
  recommend_model(model_c, users, 5)

def get_popular_movies_mock():
  """
  mock data of popular movies for devlopment purpose
  """
  mock = [
    {'userId': 135.0, 'movieId': 304.0, 'score': 5.0, 'rank': 1.0}, 
    {'userId': 135.0, 'movieId': 136359.0, 'score': 5.0, 'rank': 2.0}, 
    {'userId': 135.0, 'movieId': 134109.0, 'score': 5.0, 'rank': 3.0}, 
    {'userId': 135.0, 'movieId': 108078.0, 'score': 5.0, 'rank': 4.0}, 
    {'userId': 135.0, 'movieId': 86668.0, 'score': 5.0, 'rank': 5.0}, 
    {'userId': 135.0, 'movieId': 112512.0, 'score': 5.0, 'rank': 6.0}]
  
  return mock

def get_popular_movies(users, size):
  trained_model = model_popular(train_data, user_id, item_id, target)
  recomm = recommend_model(trained_model, [135], 6)
  recomm = recomm.to_dataframe()
  recomm = recomm.T.to_dict().values() 
  return recomm

#def get_recommendation(data ):

