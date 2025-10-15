import pytest
from pydantic import ValidationError
from app.schemas import MovieCreate, MovieUpdate, MovieResponse

class TestSchemas:
    """Test cases for Pydantic schemas"""
    
    def test_movie_create_valid(self):
        """Test valid MovieCreate schema"""
        movie_data = {
            "title": "The Matrix",
            "director": "The Wachowskis",
            "year": 1999,
            "rating": 8.7
        }
        
        movie = MovieCreate(**movie_data)
        assert movie.title == "The Matrix"
        assert movie.director == "The Wachowskis"
        assert movie.year == 1999
        assert movie.rating == 8.7
    
    def test_movie_create_invalid_title(self):
        """Test MovieCreate with invalid title"""
        with pytest.raises(ValidationError):
            MovieCreate(
                title="",  # Empty title
                director="Test Director",
                year=2000,
                rating=8.0
            )
        
        with pytest.raises(ValidationError):
            MovieCreate(
                title="A" * 201,  # Too long title
                director="Test Director", 
                year=2000,
                rating=8.0
            )
    
    def test_movie_create_invalid_director(self):
        """Test MovieCreate with invalid director"""
        with pytest.raises(ValidationError):
            MovieCreate(
                title="Test Movie",
                director="",  # Empty director
                year=2000,
                rating=8.0
            )
        
        with pytest.raises(ValidationError):
            MovieCreate(
                title="Test Movie",
                director="A" * 101,  # Too long director name
                year=2000,
                rating=8.0
            )
    
    def test_movie_create_invalid_year(self):
        """Test MovieCreate with invalid year"""
        with pytest.raises(ValidationError):
            MovieCreate(
                title="Test Movie",
                director="Test Director",
                year=1800,  # Too early
                rating=8.0
            )
        
        with pytest.raises(ValidationError):
            MovieCreate(
                title="Test Movie",
                director="Test Director",
                year=2031,  # Too late
                rating=8.0
            )
    
    def test_movie_create_invalid_rating(self):
        """Test MovieCreate with invalid rating"""
        with pytest.raises(ValidationError):
            MovieCreate(
                title="Test Movie",
                director="Test Director",
                year=2000,
                rating=-1.0  # Negative rating
            )
        
        with pytest.raises(ValidationError):
            MovieCreate(
                title="Test Movie",
                director="Test Director",
                year=2000,
                rating=11.0  # Rating too high
            )
    
    def test_movie_create_boundary_values(self):
        """Test MovieCreate with boundary values"""
        # Minimum valid values
        movie_min = MovieCreate(
            title="A",
            director="B", 
            year=1888,
            rating=0.0
        )
        assert movie_min.title == "A"
        assert movie_min.year == 1888
        assert movie_min.rating == 0.0
        
        # Maximum valid values
        movie_max = MovieCreate(
            title="A" * 200,
            director="B" * 100,
            year=2030,
            rating=10.0
        )
        assert len(movie_max.title) == 200
        assert len(movie_max.director) == 100
        assert movie_max.year == 2030
        assert movie_max.rating == 10.0
    
    def test_movie_update_valid(self):
        """Test valid MovieUpdate schema"""
        # Test with all fields
        movie_update = MovieUpdate(
            title="Updated Title",
            director="Updated Director",
            year=2020,
            rating=9.0
        )
        assert movie_update.title == "Updated Title"
        assert movie_update.director == "Updated Director"
        assert movie_update.year == 2020
        assert movie_update.rating == 9.0
        
        # Test with partial fields
        partial_update = MovieUpdate(title="Only Title Updated")
        assert partial_update.title == "Only Title Updated"
        assert partial_update.director is None
        assert partial_update.year is None
        assert partial_update.rating is None
    
    def test_movie_update_invalid_values(self):
        """Test MovieUpdate with invalid values"""
        with pytest.raises(ValidationError):
            MovieUpdate(year=1800)  # Invalid year
        
        with pytest.raises(ValidationError):
            MovieUpdate(rating=15.0)  # Invalid rating
        
        with pytest.raises(ValidationError):
            MovieUpdate(title="")  # Empty title
    
    def test_movie_response_valid(self):
        """Test valid MovieResponse schema"""
        movie_data = {
            "id": 1,
            "title": "The Matrix",
            "director": "The Wachowskis",
            "year": 1999,
            "rating": 8.7
        }
        
        movie = MovieResponse(**movie_data)
        assert movie.id == 1
        assert movie.title == "The Matrix"
        assert movie.director == "The Wachowskis"
        assert movie.year == 1999
        assert movie.rating == 8.7
    
    def test_movie_response_missing_id(self):
        """Test MovieResponse without ID"""
        with pytest.raises(ValidationError):
            MovieResponse(
                title="Test Movie",
                director="Test Director",
                year=2000,
                rating=8.0
                # Missing id
            )