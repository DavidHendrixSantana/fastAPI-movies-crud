from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import create_tables
from .routers import router

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="Movies CRUD API",
        description="A comprehensive API for managing movies with CRUD operations",
        version="2.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(router)
    
    # Root endpoint
    @app.get("/", tags=["root"])
    def read_root():
        """Welcome endpoint"""
        return {
            "message": "Welcome to Movies CRUD API v2.0",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    
    @app.get("/health", tags=["health"])
    def health_check():
        """Health check endpoint"""
        return {"status": "healthy", "version": "2.0.0"}
    
    return app

# Create tables on startup
create_tables()

# Create app instance
app = create_app()