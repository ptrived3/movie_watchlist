"""
routers.py

Swagger Documentation Quality
"""

import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status

from models import Movie, MovieCreate, MovieUpdate
from storage import read_data, write_data
from auth import verify

router = APIRouter()

DATA_FILE = "data/movies.json"


# decorator for posting data
@router.post(
        "/movies",      # URL path
        response_model = Movie,      # before returning, shape like Movie class from models
        status_code = 201,  # 201 --> created
        # swagger
        summary="Add a new movie",
        description = "Creates a new movie watchlist. This step required authentication. "
                      "Returns the created movie including its auto-generated movie id and created_at time.",
        
        responses = {
            401: {"description": "Invalid or missing credentials. Unable to authorize."},
            422: {"description": "Validation error. The request didn't match the schema"},
        },
)
def create_movie(movie: MovieCreate, username: str = Depends(verify)):
    movies = read_data(DATA_FILE)

    new_movie = Movie(
        id = str(uuid.uuid4()),
        created_at = datetime.now(),
        **movie.model_dump(),
    )

    movies.append(new_movie.model_dump(mode="json"))
    write_data(DATA_FILE, movies)

    return new_movie


# read all the values
@router.get(
        "/movies",
        response_model = list[Movie],
        summary = "List all movies",
        description = "Returns every move that is there in the watchlist. Optional pagination through skip/limit query param is allowed.",
        responses = {
            401: {"description": "Invalid or missing credentials. Unable to authorize."},
        },
)
def list_all_movies(skip: int = 0, limit: int = 50, username: str = Depends(verify)):
    movies = read_data(DATA_FILE)
    return movies[skip : skip + limit]


# get the movies summary
@router.get(
    "/movies/summary",
    summary="Get watchlist summary",
    description = "Returns the computed statistics for the movies with attributes of: total count, average, rating, and a breakdown of how many movies are under each status.",
    responses = {
        401: {"description": "Invalid or missing credentials. Unable to authorize."},
    },
)
def movies_summary(username:str = Depends(verify)):
    movies = read_data(DATA_FILE)

    total = len(movies)

    if total == 0:
        return {"total_movies": 0, "average_rating": None, "by_status": {}}
    
    # find the average ratings for that movie in the list
    tot_rating = 0
    for movie in movies:
        tot_rating += movie["rating"]
    
    avg_rating = round(tot_rating/total, 2)

    # find the 
    by_status = {}
    for movie in movies:
        status_value = movie["watch_status"]
        by_status[status_value] = 1 + by_status.get(status_value, 0)


    return {
        "total_movies": total,
        "average_rating": avg_rating,
        "by_status": by_status,
    }


# search and filter the movies
@router.get(
    "/movies/search",
    response_model = list[Movie],
    summary = "Search and filter movies",
    description = "Returns a list of movies depending on the search by status query. Filters combine, so passing both genre "
                "and watch_status returns only movies matching both.",
    responses = {
        401: {"description": "Invalid or missing credentials. Unable to authorize."},
    },
)
def search_movies(genre: str | None = None, watch_status: str | None = None, min_rating: int | None = None, username: str = Depends(verify)):
    movies = read_data(DATA_FILE)
    results = []

    for movie in movies:
        if genre is not None and movie["genre"] != genre:
            continue
        if watch_status is not None and movie["watch_status"] != watch_status:
            continue
        if min_rating is not None and movie["rating"] < min_rating:
            continue
        results.append(movie)

    return results


# get ome movie by ID
@router.get(
        "/movies/{movie_id}",
        response_model = Movie,
        summary = "Get a single movie",
        description = "Returns the informatoin for one movie based on its ID. If the movie is not found, return 404.",
        responses = {
            401: {"description": "Invalid or missing credentials. Unable to authorize."},
            404: {"description": "Movie by that ID is not found."},
        },
)
def get_movie(movie_id: str, username: str = Depends(verify)):
    movies = read_data(DATA_FILE)   # list of all the movies
    for movie in movies:        # find the movie and return it
        if movie["id"] == movie_id:
            return movie
    
    # if the movie is not found, raise a 404
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Movie not found",
    )


# update a movie
@router.patch(
        "/movies/{movie_id}",
        response_model = Movie,
        summary = "Update a movie",
        description = "Updates a movie based on the movie ID that is provided. Only change the fields that you specify. Returns 404 if the movie is not found.",
        responses = {
            401: {"description": "Invalid or missing credentials. Unable to authorize."},
            404: {"description": "Movie by that ID is not found."},
        },
)
def update_movie(movie_id: str, updates: MovieUpdate, username: str = Depends(verify)):
    movies = read_data(DATA_FILE)

    for movie in movies:        # find the movie that needs to be updates
        if movie["id"] == movie_id:
            changes = updates.model_dump(exclude_unset=True)
            movie.update(changes)
            write_data(DATA_FILE, movies)
            return movie
    
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Movie not found",
    )


# delete movie by ID
@router.delete(
    "/movies/{movie_id}",
    status_code=204,
    summary = "Delete a movie",
    description = "Removes amovie from the watchlist by its id. "
                  "Returns 404 if no movie has that id.",

    responses = {
        401: {"description": "Invalid or missing credentials. Unable to authorize."},
        404: {"description": "Movie by that ID is not found."},
    },
)
def delete_movie(movie_id: str, username: str = Depends(verify)):
    movies = read_data(DATA_FILE)

    for index, movie in enumerate(movies):        # find the movie that needs to be updates
        if movie["id"] == movie_id:
            movies.pop(index)
            write_data(DATA_FILE, movies)
            return
    
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Movie not found",
    )