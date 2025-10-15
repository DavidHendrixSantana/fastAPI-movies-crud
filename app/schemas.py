from pydantic import BaseModel, Field
from typing import Optional

class MovieBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Movie title")
    director: str = Field(..., min_length=1, max_length=100, description="Director name")
    year: int = Field(..., ge=1888, le=2030, description="Release year")
    rating: float = Field(..., ge=0.0, le=10.0, description="Movie rating")

class MovieCreate(MovieBase):
    pass

class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    director: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1888, le=2030)
    rating: Optional[float] = Field(None, ge=0.0, le=10.0)

class MovieResponse(MovieBase):
    id: int
    
    model_config = {"from_attributes": True}

class MovieListResponse(BaseModel):
    movies: list[MovieResponse]
    total: int
    skip: int
    limit: int