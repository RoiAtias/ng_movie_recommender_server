from wordcloud import WordCloud
from collections import Counter
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-interactive plotting
import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd
import base64
import tkinter as tk
from tkinter import ttk
import threading

class ReviewExtendedData:
    def __init__(self):
        pass

    def word_count(self, reviews):
        positive_reviews = reviews[reviews["sentiment"] == 'Positive']
        neutral_reviews = reviews[reviews["sentiment"] == 'Neutral']
        negative_reviews = reviews[reviews["sentiment"] == 'Negative']
        return positive_reviews, neutral_reviews, negative_reviews

    def word_cloud(self, reviews_group):
        text = ' '.join(reviews_group['content'])
        if text:
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

            img = BytesIO()
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0)
            img.seek(0)
            plt.close()

            return base64.b64encode(img.getvalue()).decode('utf-8')

    def review_common_words(self, reviews):
        common_words_dict = {}
        common_text = ' '.join(reviews['content'])
        words = common_text.split()
        if words:
            word_counts = Counter(words)
            common_words = word_counts.most_common(10)
            common_words_dict = dict(common_words)
        
        return common_words_dict

    def generate_extended_model(self, reviews):
        reviews_group = pd.DataFrame(reviews)
        positive_reviews, neutral_reviews, negative_reviews = self.word_count(reviews_group)

        positive_reviews_image = self.word_cloud(positive_reviews)
        neutral_reviews_image = self.word_cloud(neutral_reviews)
        negative_reviews_image = self.word_cloud(negative_reviews)

        positive_common_words = self.review_common_words(positive_reviews)
        neutral_common_words = self.review_common_words(neutral_reviews)
        negative_common_words = self.review_common_words(negative_reviews)

        extended_model = {
            'positive_reviews_length': len(positive_reviews),
            'neutral_reviews_length': len(neutral_reviews),
            'negative_reviews_length': len(negative_reviews),
            'positive_reviews_image': positive_reviews_image,
            'neutral_reviews_image': neutral_reviews_image,
            'negative_reviews_image': negative_reviews_image,
            'positive_common_words': positive_common_words,
            'neutral_common_words': neutral_common_words,
            'negative_common_words': negative_common_words,
        }

        return extended_model

    def run(self, reviews):
      model = self.generate_extended_model(reviews)
      return model;