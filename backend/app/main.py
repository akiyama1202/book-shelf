from fastapi import FastAPI

from app.api.routes import auth

app = FastAPI(title="Book Shelf API")

app.include_router(auth.router)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
