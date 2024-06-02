from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from movie_logic import MovieLogic
from review_extended_data import ReviewExtendedData

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

movieLogic = MovieLogic();
reviewExtendedData = ReviewExtendedData();

@app.route('/api/movies/searchSimilarMovies', methods=['POST'])
def receive_movies_array():
    data = request.get_json()
    array = data['data']
    movies = movieLogic.get_similar_movie_data(array);
    return json.dumps({"movies": movies})


@app.route('/api/movies/reviews', methods=['POST'])
def receive_reviews_array():
    data = request.get_json()
    movieName = data['data']
    reviews = movieLogic.getReviews(movieName);
    extend_data = reviewExtendedData.run(reviews);
    return json.dumps({"reviews": reviews,"extended":extend_data})

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'success', 'message': 'Test endpoint is working'})

if __name__ == '__main__':
    app.run(debug=False)
