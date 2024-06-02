import pymongo as pym

class DB:
    def __init__(self):
      client = pym.MongoClient('mongodb://localhost:27017/')
      self.db = client['movie_recommander']
 
    def get_movie_reviews(self,movie_title):
      reviews_collection = self.db['reviews']
      cursor = reviews_collection.find({'movie': movie_title})
      reviews_list = list(cursor)
      return reviews_list
    
    def update_review_sentiment(self, movie_title, new_sentiment):
        reviews_collection = self.db['reviews']
        result = reviews_collection.update_one(
            {'title': movie_title},
            {'$set': {'sentiment': new_sentiment}}
        )
        return result.modified_count
    

  







