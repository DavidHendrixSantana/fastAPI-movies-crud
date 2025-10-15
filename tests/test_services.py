import pytest
from app.schemas import MovieCreate, MovieUpdate
from app.services import MovieService
from app.database import Movie

class TestMovieService:
    """Test cases for MovieService"""
    
    def test_create_movie(self, db_session, sample_movie):
        """Test creating a new movie"""
        movie_create = MovieCreate(**sample_movie)
        movie = MovieService.create_movie(db_session, movie_create)
        
        assert movie.id is not None
        assert movie.title == sample_movie["title"]
        assert movie.director == sample_movie["director"]
        assert movie.year == sample_movie["year"]
        assert movie.rating == sample_movie["rating"]
    
    def test_get_movie_exists(self, db_session, sample_movie):
        """Test getting an existing movie"""
        movie_create = MovieCreate(**sample_movie)
        created_movie = MovieService.create_movie(db_session, movie_create)
        
        retrieved_movie = MovieService.get_movie(db_session, created_movie.id)
        
        assert retrieved_movie is not None
        assert retrieved_movie.id == created_movie.id
        assert retrieved_movie.title == sample_movie["title"]
    
    def test_get_movie_not_exists(self, db_session):
        """Test getting a non-existent movie"""
        movie = MovieService.get_movie(db_session, 999)
        assert movie is None
    
    def test_get_movies(self, db_session, sample_movies):
        """Test getting all movies with pagination"""
        # Create multiple movies
        for movie_data in sample_movies:
            movie_create = MovieCreate(**movie_data)
            MovieService.create_movie(db_session, movie_create)
        
        # Test get all movies
        movies = MovieService.get_movies(db_session)
        assert len(movies) == len(sample_movies)
        
        # Test pagination
        movies_page1 = MovieService.get_movies(db_session, skip=0, limit=2)
        assert len(movies_page1) == 2
        
        movies_page2 = MovieService.get_movies(db_session, skip=2, limit=2)
        assert len(movies_page2) == 1
    
    def test_get_movies_count(self, db_session, sample_movies):
        """Test getting total count of movies"""
        # Initially should be 0
        count = MovieService.get_movies_count(db_session)
        assert count == 0
        
        # Create movies
        for movie_data in sample_movies:
            movie_create = MovieCreate(**movie_data)
            MovieService.create_movie(db_session, movie_create)
        
        count = MovieService.get_movies_count(db_session)
        assert count == len(sample_movies)
    
    def test_update_movie_exists(self, db_session, sample_movie):
        """Test updating an existing movie"""
        movie_create = MovieCreate(**sample_movie)
        created_movie = MovieService.create_movie(db_session, movie_create)
        
        update_data = MovieUpdate(
            title="The Matrix Reloaded",
            rating=7.2
        )
        
        updated_movie = MovieService.update_movie(db_session, created_movie.id, update_data)
        
        assert updated_movie is not None
        assert updated_movie.title == "The Matrix Reloaded"
        assert updated_movie.rating == 7.2
        assert updated_movie.director == sample_movie["director"]  # Should remain unchanged
        assert updated_movie.year == sample_movie["year"]  # Should remain unchanged
    
    def test_update_movie_not_exists(self, db_session):
        """Test updating a non-existent movie"""
        update_data = MovieUpdate(title="Non-existent Movie")
        updated_movie = MovieService.update_movie(db_session, 999, update_data)
        assert updated_movie is None
    
    def test_delete_movie_exists(self, db_session, sample_movie):
        """Test deleting an existing movie"""
        movie_create = MovieCreate(**sample_movie)
        created_movie = MovieService.create_movie(db_session, movie_create)
        
        success = MovieService.delete_movie(db_session, created_movie.id)
        assert success is True
        
        # Verify movie is deleted
        deleted_movie = MovieService.get_movie(db_session, created_movie.id)
        assert deleted_movie is None
    
    def test_delete_movie_not_exists(self, db_session):
        """Test deleting a non-existent movie"""
        success = MovieService.delete_movie(db_session, 999)
        assert success is False
    
    def test_search_movies_by_title(self, db_session, sample_movies):
        """Test searching movies by title"""
        # Create movies
        for movie_data in sample_movies:
            movie_create = MovieCreate(**movie_data)
            MovieService.create_movie(db_session, movie_create)
        
        # Search for "Matrix"
        movies = MovieService.search_movies_by_title(db_session, "Matrix")
        assert len(movies) == 1
        assert "Matrix" in movies[0].title
        
        # Search for "the" (case insensitive)
        movies = MovieService.search_movies_by_title(db_session, "the")
        assert len(movies) == 1  # Only "The Matrix" contains "the"
        
        # Search for non-existent title
        movies = MovieService.search_movies_by_title(db_session, "Non-existent")
        assert len(movies) == 0
    
    def test_get_movies_by_director(self, db_session, sample_movies):
        """Test getting movies by director"""
        # Create movies
        for movie_data in sample_movies:
            movie_create = MovieCreate(**movie_data)
            MovieService.create_movie(db_session, movie_create)
        
        # Search for Christopher Nolan movies
        movies = MovieService.get_movies_by_director(db_session, "Christopher Nolan")
        assert len(movies) == 2
        
        # Search for Wachowskis movies
        movies = MovieService.get_movies_by_director(db_session, "Wachowski")
        assert len(movies) == 1
        
        # Search for non-existent director
        movies = MovieService.get_movies_by_director(db_session, "Non-existent Director")
        assert len(movies) == 0
    
    def test_get_movies_by_year_range(self, db_session, sample_movies):
        """Test getting movies by year range"""
        # Create movies
        for movie_data in sample_movies:
            movie_create = MovieCreate(**movie_data)
            MovieService.create_movie(db_session, movie_create)
        
        # Get movies from 2000-2015
        movies = MovieService.get_movies_by_year_range(db_session, 2000, 2015)
        assert len(movies) == 2  # Inception (2010) and Interstellar (2014)
        
        # Get movies from 1990-2000
        movies = MovieService.get_movies_by_year_range(db_session, 1990, 2000)
        assert len(movies) == 1  # The Matrix (1999)
        
        # Get movies from future range
        movies = MovieService.get_movies_by_year_range(db_session, 2025, 2030)
        assert len(movies) == 0