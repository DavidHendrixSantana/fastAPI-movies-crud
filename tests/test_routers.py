import pytest
from fastapi.testclient import TestClient

class TestMovieRouters:
    """Test cases for Movie API endpoints"""
    
    def test_read_root(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Movies CRUD API" in data["message"]
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
    
    def test_create_movie_success(self, client, sample_movie):
        """Test successful movie creation"""
        response = client.post("/movies/", json=sample_movie)
        assert response.status_code == 201
        
        data = response.json()
        assert data["title"] == sample_movie["title"]
        assert data["director"] == sample_movie["director"]
        assert data["year"] == sample_movie["year"]
        assert data["rating"] == sample_movie["rating"]
        assert "id" in data
    
    def test_create_movie_invalid_data(self, client):
        """Test movie creation with invalid data"""
        invalid_movie = {
            "title": "",  # Empty title
            "director": "Test Director",
            "year": 1800,  # Invalid year
            "rating": 15.0  # Invalid rating
        }
        
        response = client.post("/movies/", json=invalid_movie)
        assert response.status_code == 422
    
    def test_create_movie_missing_fields(self, client):
        """Test movie creation with missing required fields"""
        incomplete_movie = {
            "title": "Test Movie"
            # Missing director, year, rating
        }
        
        response = client.post("/movies/", json=incomplete_movie)
        assert response.status_code == 422
    
    def test_get_movies_empty(self, client):
        """Test getting movies when database is empty"""
        response = client.get("/movies/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["movies"] == []
        assert data["total"] == 0
        assert data["skip"] == 0
        assert data["limit"] == 100
    
    def test_get_movies_with_data(self, client, sample_movies):
        """Test getting movies with data in database"""
        # Create movies first
        created_movies = []
        for movie in sample_movies:
            response = client.post("/movies/", json=movie)
            assert response.status_code == 201
            created_movies.append(response.json())
        
        # Get all movies
        response = client.get("/movies/")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["movies"]) == len(sample_movies)
        assert data["total"] == len(sample_movies)
    
    def test_get_movies_with_pagination(self, client, sample_movies):
        """Test getting movies with pagination"""
        # Create movies first
        for movie in sample_movies:
            response = client.post("/movies/", json=movie)
            assert response.status_code == 201
        
        # Test pagination
        response = client.get("/movies/?skip=0&limit=2")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["movies"]) == 2
        assert data["skip"] == 0
        assert data["limit"] == 2
        assert data["total"] == len(sample_movies)
    
    def test_get_movies_search_by_title(self, client, sample_movies):
        """Test searching movies by title"""
        # Create movies first
        for movie in sample_movies:
            response = client.post("/movies/", json=movie)
            assert response.status_code == 201
        
        # Search for "Matrix"
        response = client.get("/movies/?title=Matrix")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["movies"]) == 1
        assert "Matrix" in data["movies"][0]["title"]
    
    def test_get_movies_filter_by_director(self, client, sample_movies):
        """Test filtering movies by director"""
        # Create movies first
        for movie in sample_movies:
            response = client.post("/movies/", json=movie)
            assert response.status_code == 201
        
        # Filter by Christopher Nolan
        response = client.get("/movies/?director=Christopher Nolan")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["movies"]) == 2  # Inception and Interstellar
        for movie in data["movies"]:
            assert "Christopher Nolan" in movie["director"]
    
    def test_get_movie_by_id_success(self, client, sample_movie):
        """Test getting a specific movie by ID"""
        # Create movie first
        create_response = client.post("/movies/", json=sample_movie)
        assert create_response.status_code == 201
        created_movie = create_response.json()
        
        # Get movie by ID
        response = client.get(f"/movies/{created_movie['id']}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == created_movie["id"]
        assert data["title"] == sample_movie["title"]
    
    def test_get_movie_by_id_not_found(self, client):
        """Test getting a non-existent movie by ID"""
        response = client.get("/movies/999")
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Movie not found"
    
    def test_update_movie_success(self, client, sample_movie):
        """Test successful movie update"""
        # Create movie first
        create_response = client.post("/movies/", json=sample_movie)
        assert create_response.status_code == 201
        created_movie = create_response.json()
        
        # Update movie
        update_data = {
            "title": "The Matrix Reloaded",
            "rating": 7.2
        }
        
        response = client.put(f"/movies/{created_movie['id']}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["title"] == "The Matrix Reloaded"
        assert data["rating"] == 7.2
        assert data["director"] == sample_movie["director"]  # Should remain unchanged
    
    def test_update_movie_not_found(self, client):
        """Test updating a non-existent movie"""
        update_data = {"title": "Non-existent Movie"}
        
        response = client.put("/movies/999", json=update_data)
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Movie not found"
    
    def test_update_movie_invalid_data(self, client, sample_movie):
        """Test updating movie with invalid data"""
        # Create movie first
        create_response = client.post("/movies/", json=sample_movie)
        assert create_response.status_code == 201
        created_movie = create_response.json()
        
        # Try to update with invalid data
        invalid_update = {
            "year": 1800,  # Invalid year
            "rating": 15.0  # Invalid rating
        }
        
        response = client.put(f"/movies/{created_movie['id']}", json=invalid_update)
        assert response.status_code == 422
    
    def test_delete_movie_success(self, client, sample_movie):
        """Test successful movie deletion"""
        # Create movie first
        create_response = client.post("/movies/", json=sample_movie)
        assert create_response.status_code == 201
        created_movie = create_response.json()
        
        # Delete movie
        response = client.delete(f"/movies/{created_movie['id']}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Movie deleted successfully"
        
        # Verify movie is deleted
        get_response = client.get(f"/movies/{created_movie['id']}")
        assert get_response.status_code == 404
    
    def test_delete_movie_not_found(self, client):
        """Test deleting a non-existent movie"""
        response = client.delete("/movies/999")
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Movie not found"
    
    def test_get_movies_by_year_range_success(self, client, sample_movies):
        """Test getting movies by year range"""
        # Create movies first
        for movie in sample_movies:
            response = client.post("/movies/", json=movie)
            assert response.status_code == 201
        
        # Get movies from 2000-2015
        response = client.get("/movies/search/year-range/?start_year=2000&end_year=2015")
        assert response.status_code == 200
        
        data = response.json()
        assert data["count"] == 2  # Inception and Interstellar
        assert len(data["movies"]) == 2
    
    def test_get_movies_by_year_range_invalid(self, client):
        """Test getting movies with invalid year range"""
        response = client.get("/movies/search/year-range/?start_year=2015&end_year=2000")
        assert response.status_code == 400
        
        data = response.json()
        assert "Start year must be less than or equal to end year" in data["detail"]
    
    def test_pagination_parameters_validation(self, client):
        """Test pagination parameters validation"""
        # Test negative skip
        response = client.get("/movies/?skip=-1")
        assert response.status_code == 422
        
        # Test limit exceeding maximum
        response = client.get("/movies/?limit=1001")
        assert response.status_code == 422
        
        # Test zero limit
        response = client.get("/movies/?limit=0")
        assert response.status_code == 422