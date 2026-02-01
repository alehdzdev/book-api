from contextlib import asynccontextmanager

# FastAPI
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Local
from auth.views import router as auth_router
from books.views import router as books_router
from config import settings
from db.migration import migrate_initial_data
from db.mongo import connect_to_mongo, close_mongo_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_to_mongo()
    migrate_initial_data()
    yield
    close_mongo_connection()


app = FastAPI(
    title="Book Management System",
    description="REST API to manage books information with MongoDB",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
app.include_router(books_router, prefix=settings.API_V1_PREFIX)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "book-management-api"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
