import pandas as pd 
import turicreate as tc
import os
#from sklearn.model_selection import train_test_split

file_link = "links.csv"
#file_movies_ratings = "movies_ratings.csv"
file_movies_ratings = "movies_ratings_clean.csv"
file_movies_links = "movies_links.csv"
file_movies = "movies.csv"
file_ratings = "ratings.csv"
file_tags = "tags.csv"

dir_loc = os.path.dirname(os.path.realpath(__file__))+'/../../../data/'
#link_sf = tc.SFrame.read_csv('+file_link)

movies_ratings = pd.read_csv(dir_loc+file_movies_ratings)
movies_link = pd.read_csv(dir_loc+file_link)
movies_all = pd.read_csv(dir_loc+file_movies_links)
movies = pd.read_csv(dir_loc+file_movies)
link = pd.read_csv(dir_loc+file_link)

user_id = "userId"
item_id = "movieId"
target = "rating"

# train will all data for web request
# train_data_full = movies_ratings[["userId", "movieId", "rating"]]
train_data_full = movies_ratings[["userId","movieId","Action","Adventure","Animation","Children","Comedy","Crime","Documentary","Drama","Fantasy","FilmNoir","Horror","Musical","Mystery","Romance","SciFi","Thriller","War","Western-1","NA","rating"]]
train_data_full = tc.SFrame(train_data_full)

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


#train_data, test_data = split_data(movies_ratings)

def model_popular(train_data, user_id, item_id, target):
  return tc.popularity_recommender.create(train_data,user_id=user_id,item_id=item_id)

def model_cosine(train_data, user_id, item_id, target):
  return tc.item_similarity_recommender.create(train_data,user_id=user_id,item_id=item_id, similarity_type='cosine')

def model_pearson(train_data, user_id, item_id, target):
  return tc.item_similarity_recommender.create(train_data,user_id=user_id,item_id=item_id, similarity_type='pearson')

def model_general(train_data, user_id, item_id, target):
  return tc.recommender.create(train_data, user_id=user_id, item_id=item_id, target=target)

def recommend_model(model, users, rec_size):
  recommand = model.recommend(users=users, k=rec_size)
  #recommand.print_rows(display_size)
  return recommand

def test_modeling():
  users = [135,136,137]
  train_data = movies_ratings[["userId", "movieId", "rating"]]
  train_data = tc.SFrame(train_data)
  model_po = model_popular(train_data, user_id, item_id, target)
  rm = recommend_model(model_po, users, 5)
  rm.print_rows(6)
  model_c = model_cosine(train_data, user_id, item_id, target)
  rm = recommend_model(model_c, users, 5)
  rm.print_rows(6)

def get_popular_movies_mock():
  """
  mock data of popular movies for devlopment purpose
  """
  mock = [
    {'userId': 135, 'movieId': 3851, 'score': 5.0, 'rank': 2, 'title': "I'm the One That I Want (2000)", 'imdbId': 251739}, 
    {'userId': 135, 'movieId': 8142, 'score': 5.0, 'rank': 3, 'title': 'Dead or Alive: Hanzaisha (1999)', 'imdbId': 221111}, 
    {'userId': 135, 'movieId': 136447, 'score': 5.0, 'rank': 4, 'title': 'George Carlin: You Are All Diseased (1999)', 'imdbId': 246645}, 
    {'userId': 135, 'movieId': 99, 'score': 5.0, 'rank': 5, 'title': 'Heidi Fleiss: Hollywood Madam (1995)', 'imdbId': 113283}, 
    {'userId': 135, 'movieId': 70451, 'score': 5.0, 'rank': 6, 'title': 'Max Manus (2008)', 'imdbId': 1029235}]
  mock = format_imdbid(mock)
  return mock

def get_mock_user_likes():
  mock = [
    {
      'movieId':3851,
      'rating':3
    },
    {
      'movieId':8142,
      'rating':4
    },
    {
      'movieId':136447,
      'rating':5
    },
    {
      'movieId':99,
      'rating':1
    },
    {
      'movieId':70451,
      'rating':1
    }                
  ]
  return mock

def get_popular_movies(users, size):

  trained_model = model_popular(train_data_full, user_id, item_id, target)
  recomm = recommend_model(trained_model, [135], 6)
  recomm = recomm.to_dataframe()
  recomm = pd.merge(recomm,movies_all[["movieId","title","imdbId"]], left_on ="movieId", right_on = "movieId", how="inner")
  recomm = recomm.T.to_dict().values() 
  recomm = format_imdbid(recomm)
  return recomm

def format_imdbid(items):
  for item in items:
    item["imdbId"] = format(item["imdbId"], '07d')
  return items

def get_all_movies():
  movies_list = movies.T.to_dict().values() 
  all_movie = []
  for item in movies_list:
    all_movie.append(item)

  return all_movie

def get_cosine_recomm(movie_list):
  user=9999999
  train_data_full = get_user_sf(movie_list,user)

  trained_model = model_cosine(train_data_full, user_id, item_id, target)
  recomm = recommend_model(trained_model, [user], 10)
  recomm = recomm.to_dataframe()
  recomm = pd.merge(recomm,movies_all[["movieId","title","imdbId"]], left_on ="movieId", right_on = "movieId", how="inner")
  recomm = recomm.T.to_dict().values() 
  recomm = format_imdbid(recomm)
  return recomm

def get_pearson_recomm(movie_list):
  user=9999999
  train_data_full = get_user_sf(movie_list,user)

  trained_model = model_pearson(train_data_full, user_id, item_id, target)
  recomm = recommend_model(trained_model, [user], 10)
  recomm = recomm.to_dataframe()
  recomm = pd.merge(recomm,movies_all[["movieId","title","imdbId"]], left_on ="movieId", right_on = "movieId", how="inner")
  recomm = recomm.T.to_dict().values() 
  recomm = format_imdbid(recomm)
  return recomm

def get_recomm(movie_list):
  user=9999999
  train_data_full = get_user_sf(movie_list,user)
  #selected_data = train_data_full.select_columns(['userId', 'movieId'])

  trained_model = model_general(train_data_full, user_id, item_id, target)
  recomm = recommend_model(trained_model, [user], 10)
  recomm = recomm.to_dataframe()
  recomm = pd.merge(recomm,movies_all[["movieId","title","imdbId"]], left_on ="movieId", right_on = "movieId", how="inner")
  recomm = recomm.T.to_dict().values() 
  recomm = format_imdbid(recomm)
  return recomm


def get_user_sf(movie_list,user):
  item_list = []
  for item in movie_list:
    a = movies_ratings.loc[movies_ratings['movieId'] == int(item["movieId"])]
    b = a.iloc[:1] 
    c = list(b.T.to_dict().values())[0]
    c["userId"] = user
    c["rating"] = float(item["rating"])
    item_list.append(c)

  new_df = pd.DataFrame(item_list)
  final_df = new_df[["userId","movieId","Action","Adventure","Animation","Children","Comedy","Crime","Documentary","Drama","Fantasy","FilmNoir","Horror","Musical","Mystery","Romance","SciFi","Thriller","War","Western-1","NA","rating"]]
  final_sf = train_data_full.append(tc.SFrame(final_df))
  return final_sf