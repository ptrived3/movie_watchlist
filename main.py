from fastapi import FastAPI
from routers import router


app = FastAPI(
    title="Movie Watchlist API",
    description="A REST API for tracking movies, watch status, and ratings. "
                "All endpoints need HTTP Basic authentication.",
    version="1.0.0",
)

app.include_router(router)

@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok"}
