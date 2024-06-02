import os
import asyncio
import logging
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import spacy
import re
import nltk 
from PyMovieDb import IMDB
from tmdbv3api import Movie, TMDb
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from review_sentiment_analysis import ReviewSentimentAnalysis
import requests
from bs4 import BeautifulSoup


class MovieLogic():  
   def __init__(self):
      self.movie = Movie()
      self.tmdb = TMDb()
      self.imdb = IMDB()
      self.review_sentiment_analysis = ReviewSentimentAnalysis()
      self.tmdb.api_key = '3d832eff4f226a9a299badeb3d656d7e'
      logging.getLogger('asyncio').setLevel(logging.WARNING)
      
   def get_credits_movies(self,movieId): # Get the similar movies based on genres and keywords.
        credits_movie = []
        creditsMovie = self.movie.credits(movieId)
        if (creditsMovie['cast'] != {}):
           return creditsMovie['cast'];
        else: 
           pass

   def get_similar_movies(self,movies_title): # Get the similar movies based on genres and keywords.
        movies_tmdb = []
        for title in movies_title:
            search = self.movie.search(title)
            total_results = search['total_results']
            if (total_results != 0) :
               movies_tmdb.append(search[0])
            else: 
                pass
           
            
        for movie in movies_tmdb:  
            similar = self.movie.recommendations(movie.id)
            first_3_items = []
            for i in range(3):
               first_3_items.append(similar['results'][i])
                
        return first_3_items;


   def get_movie_reviews(self,movieId):
         reviews = []
         max_item = 50
         start_url = f'https://www.imdb.com/title/{movieId}/reviews?ref_=tt_urv'
         link = f'https://www.imdb.com/title/{movieId}/reviews/_ajax'
        
         params = {
                'ref_': 'undefined',
                'paginationKey': ''
         }

         with requests.Session() as s:
            s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
            res = s.get(start_url)

            count = 0
            while count < max_item:
                soup = BeautifulSoup(res.text,"lxml")
                for item in soup.select(".review-container"):
                    reviewer_name = item.select_one("span.display-name-link > a").get_text(strip=True)
                    content = item.select_one("div.content > div.text.show-more__control").get_text(strip=True)
                    title = item.select_one("div.review-container > div.lister-item-content > a").get_text(strip=True)
                    date = item.select_one("div.display-name-date > span.review-date").get_text(strip=True)
                    rating_element  = item.select_one("div.lister-item-content > div.ipl-ratings-bar > span > span:nth-child(2)")
                    rating = rating_element.get_text(strip=True) if rating_element is not None else None
                    liked = True if rating != None and (int(rating) > 4) else False
                    
                    model = {
                             'content': content,
                             'title': title,
                             'author': reviewer_name,
                             'date': date,
                             'rating': rating,
                             'liked' : liked
                    }
   
                    reviews.append(model)
                    count += 1
                    if count == max_item:
                        break
       
                try:
                    pagination_key = soup.select_one(".load-more-data[data-key]").get("data-key")
                except AttributeError:
                    break
                params['paginationKey'] = pagination_key
                res = s.get(link,params=params)
   
         return reviews;


   def get_movie_id_imdb(self,movie_title):
         result = self.imdb.search(movie_title)
         data = json.loads(result)
         if 'results' in data and data['results']:  # Check if 'results' exist and not empty
            movie_match = data['results'][0]
            if 'id' in movie_match:
                return movie_match['id']
         return None  # Return None if no match found or data structure is unexpected

   def get_similar_movie_data(self,movies_title):
      similar_movies = self.get_similar_movies(movies_title);
      movies_items = []
      for movie in similar_movies:
          movie_item = {
              'id': movie["id"],
              'poster_path':movie["poster_path"],
              'title': movie["title"],
              'overview': movie["overview"],
              'release_date': movie["release_date"],
              'original_language':movie["original_language"],
              }
          movies_items.append(movie_item)
          
      return movies_items;

   def getReviews(self,movie_name):
      reviews = self.get_movie_reviews(self.get_movie_id_imdb(movie_name));
      working_reviews = self.review_sentiment_analysis.run(reviews)
      return working_reviews;

   def run(self,movies_title):
      similar_movies = self.get_similar_movies(movies_title);
      reviews = self.getReviews(similar_movies);
      working_reviews = self.review_sentiment_analysis.run(reviews)
      return working_reviews;


if __name__ == '__main__':
   movieLogic = MovieLogic();
   movies = movieLogic.run(['Borat Subsequent Moviefilm']);
    