from fastapi import FastAPI

from app.api.routes import auth, books, tags

app = FastAPI(title="Book Shelf API")

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(tags.router)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
