from sqlalchemy.orm import Session
from sqlalchemy import func
from .database import Movie
from .schemas import MovieCreate, MovieUpdate
from typing import List, Optional

class MovieService:
    @staticmethod
    def create_movie(db: Session, movie: MovieCreate) -> Movie:
        """Create a new movie"""
        db_movie = Movie(**movie.model_dump())
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        return db_movie
    
    @staticmethod
    def get_movie(db: Session, movie_id: int) -> Optional[Movie]:
        """Get a movie by ID"""
        return db.query(Movie).filter(Movie.id == movie_id).first()
    
    @staticmethod
    def get_movies(db: Session, skip: int = 0, limit: int = 100) -> List[Movie]:
        """Get all movies with pagination"""
        return db.query(Movie).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_movies_count(db: Session) -> int:
        """Get total count of movies"""
        return db.query(func.count(Movie.id)).scalar()
    
    @staticmethod
    def update_movie(db: Session, movie_id: int, movie_update: MovieUpdate) -> Optional[Movie]:
        """Update an existing movie"""
        db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if not db_movie:
            return None
        
        update_data = movie_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_movie, field, value)
        
        db.commit()
        db.refresh(db_movie)
        return db_movie
    
    @staticmethod
    def delete_movie(db: Session, movie_id: int) -> bool:
        """Delete a movie by ID"""
        db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if not db_movie:
            return False
        
        db.delete(db_movie)
        db.commit()
        return True
    
    @staticmethod
    def search_movies_by_title(db: Session, title: str, skip: int = 0, limit: int = 100) -> List[Movie]:
        """Search movies by title"""
        return db.query(Movie).filter(
            Movie.title.ilike(f"%{title}%")
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_movies_by_director(db: Session, director: str, skip: int = 0, limit: int = 100) -> List[Movie]:
        """Get movies by director"""
        return db.query(Movie).filter(
            Movie.director.ilike(f"%{director}%")
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_movies_by_year_range(db: Session, start_year: int, end_year: int) -> List[Movie]:
        """Get movies within a year range"""
        return db.query(Movie).filter(
            Movie.year >= start_year,
            Movie.year <= end_year
        ).all()