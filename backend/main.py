"""
Aplicación principal FastAPI
"""

from contextlib import asynccontextmanager

# FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Local
from auth_routes import router as auth_router
from books_routes import router as books_router
from core.config import settings
from database import connect_to_mongo, close_mongo_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Maneja el ciclo de vida de la aplicación
    """
    connect_to_mongo()
    yield
    close_mongo_connection()


app = FastAPI(
    title="Sistema de Gestión de Libros",
    description="API REST para gestionar información de libros con MongoDB",
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


@app.get("/")
async def root():
    """
    Endpoint raíz de la API
    """
    return {
        "message": "Bienvenido al Sistema de Gestión de Libros",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    """
    Endpoint para verificar el estado de la API
    """
    return {"status": "healthy", "service": "book-management-api"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
