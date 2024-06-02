import aiohttp ,json,os
import logging
import re
import requests
from nltk.tokenize.toktok import ToktokTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string,time
from textblob import TextBlob
from concurrent.futures import ThreadPoolExecutor

class ReviewSentimentAnalysis:
   
     def __init__(self):
       self.tokenizer=ToktokTokenizer()
       self.stopword_list=nltk.corpus.stopwords.words('english')
       nltk.download('vader_lexicon')
       nltk.download('punkt')
       nltk.download('stopwords')
       nltk.download('wordnet')
       self.sid = SentimentIntensityAnalyzer()
       self.tokenizer = ToktokTokenizer()
       
     #removing the tags html
     def remove_html_tags(self,review):
         pattern = r'[^a-zA-Z0-9\s]'
         review = re.sub(pattern,'',review)
         return review
     
     #removing the url
     def remove_url(self,text):
        pattern = re.compile(r'https?://\S+|www\.\S+')
        return pattern.sub(r'',text)
    
     # removing punctuation(text):
     def remove_punctuation(self,review):
        return review.translate(str.maketrans('','',string.punctuation))
    
     # removing emoji
     def remove_emoji(self,review):
        emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', review)
 
     #removing the stopwords
     def remove_stopwords(self,text, is_lower_case=False):
        tokens = self.tokenizer.tokenize(text)
        tokens = [token.strip() for token in tokens]
        if is_lower_case:
            filtered_tokens = [token for token in tokens if token not in self.stopword_list]
        else:
            filtered_tokens = [token for token in tokens if token.lower() not in self.stopword_list]
            
        filtered_text = ' '.join(filtered_tokens)   
        
        return filtered_text
    
     #Define function for removing special characters
     def remove_special_characters(self,text, remove_digits=True):
            pattern=r'[^a-zA-z0-9\s]'
            text=re.sub(pattern,'',text)
            return text
     
     # def correct_spelling(self,review):
     #    blob = TextBlob(review)
     #    corrected_review = blob.correct()
     #    return str(corrected_review)
  
     def preprocess_text(self,review):
        working_review = ''
        #lower case
        working_review = review.lower;
        #removing htmltag 
        working_review = self.remove_html_tags(review);
        #removing url 
        working_review = self.remove_url(working_review);
        # removing emoji
        working_review = self.remove_emoji(working_review);
        # Removing special characters 
        working_review = self.remove_special_characters(working_review)
        # Removing stop words
        working_review = self.remove_stopwords(working_review)
        # Correct spelling TODO !!
        # working_review = self.correct_spelling(working_review)
        #return working_review
        return working_review;

     def calculate_sentiment(self,text):
        scores = self.sid.polarity_scores(text)
        if scores['compound'] >= 0.05:
            sentiment = 'Positive'
        elif scores['compound'] <= -0.05:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        return sentiment

     def create_reviews_text_proceesess_with_sentiment(self,reviews):
        for review in reviews:
           temp_review = (self.preprocess_text(review['content']))
           review['content'] = temp_review;
           review['review_length'] = len(word_tokenize(review['content']))
           review['sentiment'] = self.calculate_sentiment(review['content'])
        return reviews;

     def run(self,reviews):
         try:
            return self.create_reviews_text_proceesess_with_sentiment(reviews);
         except BaseException as err:
            logging.error("MovieRecommenderService: Error Run Movie Recommender Service - {0}".format(err))
         finally:
            logging.debug("ReviewSentimentAnalysis: finished")
        
     def getAppSettings(self) -> dict:
        try:
          if os.path.isfile("appsettings.json"):
             with open("appsettings.json") as f:
                  ret = json.load(f)
          return ret
        except BaseException as err:
          logging.error("ReviewSentimentAnalysis: Error getConf - {0}".format(err))




