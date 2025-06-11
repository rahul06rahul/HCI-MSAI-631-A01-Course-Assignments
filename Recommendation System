import React, { useState, useEffect } from 'react';
import { Star, Search, Film, User, TrendingUp, Heart } from 'lucide-react';

const MovieRecommendationSystem = () => {
  const [currentUser, setCurrentUser] = useState('user1');
  const [searchQuery, setSearchQuery] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [userRatings, setUserRatings] = useState({});
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // Sample movie database with genres and features
  const movies = {
    1: { title: "The Matrix", genre: "Sci-Fi", year: 1999, description: "A computer programmer discovers reality is a simulation." },
    2: { title: "Inception", genre: "Sci-Fi", year: 2010, description: "A thief enters people's dreams to steal secrets." },
    3: { title: "The Godfather", genre: "Crime", year: 1972, description: "The story of a powerful crime family." },
    4: { title: "Pulp Fiction", genre: "Crime", year: 1994, description: "Interconnected stories of crime in Los Angeles." },
    5: { title: "Forrest Gump", genre: "Drama", year: 1994, description: "The extraordinary life of a simple man." },
    6: { title: "The Shawshank Redemption", genre: "Drama", year: 1994, description: "Hope and friendship in prison." },
    7: { title: "Interstellar", genre: "Sci-Fi", year: 2014, description: "A journey through space and time to save humanity." },
    8: { title: "Goodfellas", genre: "Crime", year: 1990, description: "The rise and fall of a mob associate." },
    9: { title: "Titanic", genre: "Romance", year: 1997, description: "A love story aboard the doomed ship." },
    10: { title: "Avatar", genre: "Sci-Fi", year: 2009, description: "Humans colonize an alien world." },
    11: { title: "The Dark Knight", genre: "Action", year: 2008, description: "Batman faces his greatest challenge." },
    12: { title: "Casablanca", genre: "Romance", year: 1942, description: "Love and sacrifice in wartime Morocco." }
  };

  // Sample user rating data (collaborative filtering foundation)
  const initialRatings = {
    user1: { 1: 5, 2: 4, 3: 5, 7: 4, 11: 5 },
    user2: { 1: 4, 2: 5, 4: 4, 8: 5, 11: 4 },
    user3: { 3: 5, 4: 5, 5: 4, 6: 5, 8: 4 },
    user4: { 5: 5, 6: 4, 9: 5, 12: 4 },
    user5: { 1: 3, 7: 4, 10: 5, 11: 3 },
    user6: { 2: 5, 7: 5, 10: 4, 1: 4 }
  };

  useEffect(() => {
    setUserRatings(initialRatings);
    generateRecommendations(currentUser, initialRatings);
  }, []);

  // Cosine similarity calculation for user-based collaborative filtering
  const calculateCosineSimilarity = (ratings1, ratings2) => {
    const commonMovies = Object.keys(ratings1).filter(movie => ratings2[movie]);
    
    if (commonMovies.length === 0) return 0;

    const sum1 = commonMovies.reduce((sum, movie) => sum + ratings1[movie] * ratings1[movie], 0);
    const sum2 = commonMovies.reduce((sum, movie) => sum + ratings2[movie] * ratings2[movie], 0);
    const sumProducts = commonMovies.reduce((sum, movie) => sum + ratings1[movie] * ratings2[movie], 0);

    const denominator = Math.sqrt(sum1) * Math.sqrt(sum2);
    return denominator === 0 ? 0 : sumProducts / denominator;
  };

  // Enhanced recommendation algorithm combining collaborative filtering with content-based features
  const generateRecommendations = (userId, ratingsData) => {
    setIsLoading(true);
    const userRatings = ratingsData[userId] || {};
    
    // Calculate user similarities
    const similarities = {};
    Object.keys(ratingsData).forEach(otherUser => {
      if (otherUser !== userId) {
        similarities[otherUser] = calculateCosineSimilarity(userRatings, ratingsData[otherUser]);
      }
    });

    // Find most similar users
    const sortedSimilarUsers = Object.entries(similarities)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 3);

    // Generate recommendations based on similar users
    const movieScores = {};
    const userMovies = new Set(Object.keys(userRatings).map(String));

    sortedSimilarUsers.forEach(([similarUser, similarity]) => {
      Object.entries(ratingsData[similarUser]).forEach(([movieId, rating]) => {
        if (!userMovies.has(movieId)) {
          if (!movieScores[movieId]) {
            movieScores[movieId] = { score: 0, count: 0 };
          }
          movieScores[movieId].score += rating * similarity;
          movieScores[movieId].count += similarity;
        }
      });
    });

    // Content-based enhancement: boost scores for movies in liked genres
    const likedGenres = {};
    Object.keys(userRatings).forEach(movieId => {
      if (userRatings[movieId] >= 4) {
        const genre = movies[movieId]?.genre;
        if (genre) {
          likedGenres[genre] = (likedGenres[genre] || 0) + 1;
        }
      }
    });

    // Calculate final recommendations
    const recommendations = Object.entries(movieScores)
      .map(([movieId, data]) => {
        let score = data.count > 0 ? data.score / data.count : 0;
        
        // Genre boost
        const movie = movies[movieId];
        if (movie && likedGenres[movie.genre]) {
          score *= (1 + likedGenres[movie.genre] * 0.1);
        }

        return {
          movieId: parseInt(movieId),
          movie: movies[movieId],
          score: score,
          confidence: Math.min(data.count, 1)
        };
      })
      .filter(rec => rec.movie)
      .sort((a, b) => b.score - a.score)
      .slice(0, 6);

    setTimeout(() => {
      setRecommendations(recommendations);
      setIsLoading(false);
    }, 1000);
  };

  const rateMovie = (movieId, rating) => {
    const newRatings = {
      ...userRatings,
      [currentUser]: {
        ...userRatings[currentUser],
        [movieId]: rating
      }
    };
    setUserRatings(newRatings);
    generateRecommendations(currentUser, newRatings);
  };

  const StarRating = ({ rating, onRate, movieId }) => {
    return (
      <div className="flex space-x-1">
        {[1, 2, 3, 4, 5].map(star => (
          <Star
            key={star}
            className={`w-5 h-5 cursor-pointer transition-colors ${
              star <= rating ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300 hover:text-yellow-400'
            }`}
            onClick={() => onRate(movieId, star)}
          />
        ))}
      </div>
    );
  };

  const filteredMovies = Object.entries(movies).filter(([id, movie]) =>
    movie.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    movie.genre.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 via-blue-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Film className="w-8 h-8 text-purple-600 mr-3" />
            <h1 className="text-4xl font-bold text-gray-800">AI Movie Recommender</h1>
          </div>
          <p className="text-gray-600 text-lg">
            Powered by Collaborative Filtering + Content-Based AI
          </p>
        </div>

        {/* User Selection */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center">
              <User className="w-5 h-5 text-blue-600 mr-2" />
              <h2 className="text-xl font-semibold text-gray-800">Select User Profile</h2>
            </div>
            <select
              value={currentUser}
              onChange={(e) => {
                setCurrentUser(e.target.value);
                generateRecommendations(e.target.value, userRatings);
              }}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {Object.keys(userRatings).map(user => (
                <option key={user} value={user}>
                  {user.charAt(0).toUpperCase() + user.slice(1)}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Recommendations Section */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <div className="flex items-center mb-6">
            <TrendingUp className="w-6 h-6 text-green-600 mr-3" />
            <h2 className="text-2xl font-bold text-gray-800">Recommended for You</h2>
          </div>
          
          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
              <span className="ml-3 text-gray-600">Analyzing your preferences...</span>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {recommendations.map(({ movieId, movie, score, confidence }) => (
                <div key={movieId} className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-5 border border-purple-200 hover:shadow-md transition-shadow">
                  <div className="flex justify-between items-start mb-3">
                    <h3 className="text-lg font-semibold text-gray-800 flex-1">{movie.title}</h3>
                    <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded-full ml-2">
                      {movie.genre}
                    </span>
                  </div>
                  <p className="text-gray-600 text-sm mb-3">{movie.description}</p>
                  <div className="flex justify-between items-center">
                    <div className="text-sm text-gray-500">
                      Score: {score.toFixed(2)} • Confidence: {(confidence * 100).toFixed(0)}%
                    </div>
                    <Heart className="w-5 h-5 text-red-400" />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Movie Library */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center">
              <Search className="w-6 h-6 text-blue-600 mr-3" />
              <h2 className="text-2xl font-bold text-gray-800">Movie Library</h2>
            </div>
            <input
              type="text"
              placeholder="Search movies or genres..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent w-64"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {filteredMovies.map(([id, movie]) => {
              const currentRating = userRatings[currentUser]?.[id] || 0;
              return (
                <div key={id} className="bg-gray-50 rounded-lg p-4 hover:bg-gray-100 transition-colors">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-semibold text-gray-800 text-sm">{movie.title}</h3>
                    <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                      {movie.year}
                    </span>
                  </div>
                  <p className="text-xs text-gray-600 mb-3">{movie.genre}</p>
                  <StarRating
                    rating={currentRating}
                    onRate={rateMovie}
                    movieId={parseInt(id)}
                  />
                </div>
              );
            })}
          </div>
        </div>

        {/* System Info */}
        <div className="mt-8 bg-blue-50 rounded-xl p-6 border border-blue-200">
          <h3 className="text-lg font-semibold text-blue-800 mb-3">How It Works</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-700">
            <div>
              <strong>Collaborative Filtering:</strong> Finds users with similar preferences using cosine similarity and recommends movies they enjoyed.
            </div>
            <div>
              <strong>Content-Based Enhancement:</strong> Boosts recommendations for movies in genres you've previously rated highly.
            </div>
          </div>
          <p className="text-xs text-blue-600 mt-3">
            Based on collaborative filtering techniques popularized by the Netflix Prize competition, enhanced with content-based features.
          </p>
        </div>
      </div>
    </div>
  );
};

export default MovieRecommendationSystem;
