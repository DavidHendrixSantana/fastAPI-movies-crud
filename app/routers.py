from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from .database import get_db
from .schemas import MovieCreate, MovieUpdate, MovieResponse, MovieListResponse
from .services import MovieService

router = APIRouter(
    prefix="/movies",
    tags=["movies"]
)

@router.post("/", response_model=MovieResponse, status_code=201)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    """Create a new movie"""
    try:
        return MovieService.create_movie(db, movie)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating movie: {str(e)}")

@router.get("/", response_model=MovieListResponse)
def read_movies(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    title: Optional[str] = Query(None, description="Search by title"),
    director: Optional[str] = Query(None, description="Filter by director"),
    db: Session = Depends(get_db)
):
    """Get all movies with optional filtering and pagination"""
    if title:
        movies = MovieService.search_movies_by_title(db, title, skip, limit)
    elif director:
        movies = MovieService.get_movies_by_director(db, director, skip, limit)
    else:
        movies = MovieService.get_movies(db, skip, limit)
    
    total = MovieService.get_movies_count(db)
    
    return MovieListResponse(
        movies=movies,
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/{movie_id}", response_model=MovieResponse)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    """Get a specific movie by ID"""
    movie = MovieService.get_movie(db, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, movie_update: MovieUpdate, db: Session = Depends(get_db)):
    """Update an existing movie"""
    movie = MovieService.update_movie(db, movie_id, movie_update)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    """Delete a movie"""
    success = MovieService.delete_movie(db, movie_id)
    if not success:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}

@router.get("/search/year-range/")
def get_movies_by_year_range(
    start_year: int = Query(..., description="Start year"),
    end_year: int = Query(..., description="End year"),
    db: Session = Depends(get_db)
):
    """Get movies within a specific year range"""
    if start_year > end_year:
        raise HTTPException(status_code=400, detail="Start year must be less than or equal to end year")
    
    movies = MovieService.get_movies_by_year_range(db, start_year, end_year)
    return {"movies": movies, "count": len(movies)}