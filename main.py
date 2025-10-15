"""
Movies CRUD API - Entry Point
Legacy main.py file - now imports from the refactored app module
"""

from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)