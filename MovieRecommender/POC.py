# from PyMovieDb import IMDB
# import json,os
# import requests
# from bs4 import BeautifulSoup
# from tmdbv3api import Movie, TMDb
# import csv
# import json
# from collections import defaultdict
# from db import DB
# from movie_recommender_service import MovieRecommenderService
# import asyncio

# class POC:
#     def __init__(self):
#       self.conf = self.getAppSettings()
#       self.imdb = IMDB()
#       self.tmdb = TMDb()
#       self.movie = Movie()
#       self.db = DB()
#       self.tmdb.api_key = '3d832eff4f226a9a299badeb3d656d7e'
#       self.movies_review_cache = []
    
#     def getAppSettings(self) -> dict:
#         try:
#           if os.path.isfile("appsettings.json"):
#              with open("appsettings.json") as f:
#                   ret = json.load(f)
#           return ret
#         except BaseException as err:
#           logging.error("MovieRecommenderService: Error getConf - {0}".format(err))

      
#     def save_to_csv(self,movies_review):
#         csv_file_name = "output.csv"
#         keys = movies_review[0][0].keys()
#         with open(csv_file_name, "w", newline="", encoding="utf-8") as csv_file:
#             writer = csv.writer(csv_file)
#             writer.writerow(keys)
#             for movie_review in movies_review:
#                 for review in movie_review:
#                     writer.writerow([review[key] for key in keys])
            
#     def remove_parentheses(self,title):
#         idx = title.rfind('(')
#         if idx != -1:
#             title = title[:idx].rstrip() 
#         return title
      
#     def get_similar_movies(self,movies_title): # Get the similar movies based on genres and keywords.
#         movies_ids_tmdb = []
#         similar_movies_title = []
#         for title in movies_title:
#             search = self.movie.search(title)[0]
#             movies_ids_tmdb.append(search.id)
            
#         for movie_id in movies_ids_tmdb:  
#             similar = self.movie.similar(movie_id)
            
#             first_3_items = []

#             for i in range(3):
#                first_3_items.append(similar['results'][i])
#                similar_movies_title.append(similar['results'][i].title)
                
#         return similar_movies_title;
      
#     def get_movie_reviews(self,movieId):
#          reviews = []
#          start_url = f'https://www.imdb.com/title/{movieId}/reviews?ref_=tt_urv'
#          link = f'https://www.imdb.com/title/{movieId}/reviews/_ajax'
         
#          params = {
#                 'ref_': 'undefined',
#                 'paginationKey': ''
#          }

#          with requests.Session() as s:
#             s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
#             res = s.get(start_url)

#             while True:
#                 soup = BeautifulSoup(res.text,"lxml")
#                 for item in soup.select(".review-container"):
#                     reviewer_name = item.select_one("span.display-name-link > a").get_text(strip=True)
#                     content = item.select_one("div.content > div.text.show-more__control").get_text(strip=True)
#                     title = item.select_one("div.review-container > div.lister-item-content > a").get_text(strip=True)
#                     date = item.select_one("div.display-name-date > span.review-date").get_text(strip=True)
#                     rating_element  = item.select_one("div.lister-item-content > div.ipl-ratings-bar > span > span:nth-child(2)")
#                     rating = rating_element.get_text(strip=True) if rating_element is not None else None
                    
#                     model = {
#                              'content': content,
#                              'title': title,
#                              'author': reviewer_name,
#                              'date': date,
#                              'rating': rating,
#                     }
                    
#                     reviews.append(model)

#                 try:
#                     pagination_key = soup.select_one(".load-more-data[data-key]").get("data-key")
#                 except AttributeError:
#                     break
#                 params['paginationKey'] = pagination_key
#                 res = s.get(link,params=params)
            
#          return reviews;

#     def sum_nested_array_items(self,movie_reviews):
#         total_sum = 0
#         for movie_review in movie_reviews:
#             for review in movie_review:   
#                    total_sum += 1
#         return total_sum
    
#     def get_movie_id_imdb(self,movie_title):
#          result = self.imdb.search(movie_title)
#          data = json.loads(result)
#          if 'results' in data and data['results']:  # Check if 'results' exist and not empty
#             movie_match = data['results'][0]
#             if 'id' in movie_match:
#                 return movie_match['id']
#          return None  # Return None if no match found or data structure is unexpected
   
#     def create_db(self):
#         # combined_reviews = defaultdict(list)
#         combined_reviews =[]
#         json_files = ['data_set\part-01.json', 'data_set\part-02.json', 'data_set\part-03.json','data_set\part-04.json', 'data_set\part-05.json', 'data_set\part-06.json']
#         # Loop through each file
#         for file_name in json_files:
#             with open(file_name, 'r') as file:
#                 data = json.load(file)
#                 # Loop through each review in the file
#                 for review in data:
#                     review['movie'] = self.remove_parentheses(review['movie'])
#                     # review['movie_id_imdb'] = self.get_movie_id_imdb(review['movie'])
#                     combined_reviews.append(review)
#                     # movie_name = self.remove_parentheses(review['movie'])  # Apply remove_parentheses function
#                     # Append the review to the list of reviews for this movie
#                     # combined_reviews[movie_name].append(review)

#         # combined_reviews = dict(combined_reviews)
        
#         # Write combined reviews to CSV
#         with open('combined_reviews.json', 'w') as json_file:
#             json.dump(combined_reviews, json_file, indent=4) 
#         print('roi')
        
#     def read_cache(self):
#         with open('combined_reviews.json', 'r') as json_file:
#             self.movies_review_cache = json.load(json_file)
            
#     def find_movies_cache(self,movies_title):
#         reviews_for_movies = {}
#         for movie_name in movies_title:
#             if movie_name in self.movies_review_cache:
#                 reviews_for_movies[movie_name] = self.movies_review_cache[movie_name]
#             else:
#                 reviews_for_movies[movie_name] = []
#         return reviews_for_movies
    
  
    
#     def run(self):
#        #  # Read the contents of the JSON file
#        # with open('combined_reviews.json', 'r') as json_file:
#        #      json_content = json.load(json_file)
            
#        # first_two_objects = json_content[:2]

#        #  # Write each JSON object to a separate line
#        # with open('first_two_objects.json', 'w') as output_file:
#        #      json.dump(first_two_objects, output_file, indent=4)
        
#        #self.create_db();
#        movie_reviews = []
#        movies_title_input = ['Borat Subsequent Moviefilm', 'The Hangover 3', 'Jojo Rabbit']
#        movies = []
       
#        print('Welcome to the movie recommender project')
       
#        print('----------------------------------------------------------')
#        print('Step 1 - The user selects 3 movies he has watched recently')
#        print('----------------------------------------------------------')
       
#        print('Received movies :')
       
#        # DB
#        for movie in movies_title_input:
#            print('')
#            print('- ' + movie)

       
#        print('-----------------------------------------------------------------------------------------------------------')
#        print('Step 2 - The system makes a GET call to the API to get identification information about the selected movies')
#        print('-----------------------------------------------------------------------------------------------------------')
       
#        print('')

#        print('-------------------------------------------------------------------------------------')
#        print('Step 3 - the system issues a GET call to the API and receives 3-5 recommended movies')
#        print('-------------------------------------------------------------------------------------')
       
#        movies_title_similar = self.get_similar_movies(movies_title_input);  # TODO: Change it only the first 10
       
#        print('Received movies :')
       
#        # DB
#        for movie in movies_title_similar:
#            print('')
#            print('- ' + movie)
      

#        # API
#        # for movie in movies_title:
#        #     print('')
#        #     print('- ' + movie)
#        #     result = self.imdb.search(movie)
#        #     data = json.loads(result)
#        #     movie_match = data['results'][0]
#        #     model = {
#        #                   'id': str(movie_match['id']),
#        #                   'title': movie_match['name']
#        #             }
#        #     movies.append(model)
           
#        print('---------------------------------------------------------------------------------------------------------')
#        print('Step 4 - The system makes a GET call to the API to receive all reviews of the received recommended movies')
#        print('---------------------------------------------------------------------------------------------------------')
       
      
#        # print(json.dumps(movies, indent=4))

#        print('')
#        print('-> The system collects all the reviews for the selected movies. Please wait a few minutes ...') 
#        print('')
       
#        # ---------------------DB---------------------- #
       
#        for movie in movies_title_similar:
#           print('') 
#           reviews = self.db.get_movie_reviews(movie)
#           if reviews:
#             print(f"Added {len(reviews)} reviews for {movie}")
#             movie_reviews.append(reviews)
#           else:
#             print(f"There is no review for the movie - {movie}")
       

#        # ---------------------API---------------------- #
#        # for movie in movies:
#        #      print('') 
#        #      reviews = self.get_movie_reviews(movie['id'])
#        #      print(f"Added {len(reviews)} reviews for {movie['title']}")
#        #      movie_reviews.append(reviews)
            
#        print('')     
#        print('A movie review for example:')
#        print(json.dumps(movie_reviews[0][0]['review_detail'], indent=4))
        
            
#        print('')
#        print(f'The total number of reviews for the three movie : {self.sum_nested_array_items(movie_reviews)}')   
#        print('')
       
#        print('------------------------------------------')
#        print('Step 5 - Running the recommender algorithm')
#        print('------------------------------------------')
       
#        movieRecommenderService = MovieRecommenderService();
#        movieRecommenderService.run(movie_reviews);
       
#        print('')
       
#        print('')
#        print(f'Saving all the reviews of the recommended movies in a csv file')   
#        print('')

#        self.save_to_csv(movie_reviews);
       
       
#        print('-----------------------------------------------------------------------------------------------------------------------')
#        print('Step 6 - The user gets the most recommended movie for him according to the reviews that the remomender algorithms found')
#        print('-----------------------------------------------------------------------------------------------------------------------')


#        print('Thanks.')
#        print('')
#        print('')
       
# if __name__ == '__main__':
#   service = POC()
#   service.run()
      
           

            
       




