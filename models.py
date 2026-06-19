from pydantic import BaseModel
# for created_at timestamp
from datetime import datetime
# for MovieUpdate 
from typing import Optional 

# for creating a new movie 
class MovieCreate(BaseModel):
    title: str
    genre: str
    release_year: int
    watch_status: str 
    rating: int

# for updating an existing movie 
class MovieUpdate(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    release_year: Optional[int] = None
    watch_status: Optional[str] = None
    rating: Optional[int] = None

# for returning a movie data to the user
class Movie(BaseModel):
    id: str
    title: str
    genre: str
    release_year: int
    watch_status: str
    rating: int
    created_at: datetime 