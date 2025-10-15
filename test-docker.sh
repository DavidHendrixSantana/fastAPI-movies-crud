#!/bin/bash

echo "=== Movies CRUD API - Docker Container Test ==="
echo ""

echo "🐳 Checking Docker container status..."
docker-compose ps

echo ""
echo "📋 Container logs (last 10 lines):"
docker-compose logs --tail=10 movies-api

echo ""
echo "🏥 Testing API Health (using container's internal requests):"
docker exec movies-crud-api python -c "
import requests
try:
    response = requests.get('http://localhost:8000/health')
    print(f'✅ Health check: {response.status_code} - {response.json()}')
except Exception as e:
    print(f'❌ Health check failed: {e}')
"

echo ""
echo "🎬 Testing Movies API:"
docker exec movies-crud-api python -c "
import requests
import json

try:
    # Test create movie
    movie_data = {'title': 'The Matrix', 'director': 'The Wachowskis', 'year': 1999, 'rating': 8.7}
    response = requests.post('http://localhost:8000/movies/', json=movie_data)
    if response.status_code == 201:
        print('✅ Movie created successfully')
        movie = response.json()
        print(f'   Created movie ID: {movie[\"id\"]} - {movie[\"title\"]}')
        
        # Test get movies
        response = requests.get('http://localhost:8000/movies/')
        if response.status_code == 200:
            data = response.json()
            print(f'✅ Retrieved {data[\"total\"]} movies')
        else:
            print(f'❌ Failed to get movies: {response.status_code}')
    else:
        print(f'❌ Failed to create movie: {response.status_code} - {response.text}')
        
except Exception as e:
    print(f'❌ API test failed: {e}')
"

echo ""
echo "🌐 API is available at:"
echo "   - Main API: http://localhost:8000"
echo "   - Interactive Docs: http://localhost:8000/docs"
echo "   - ReDoc: http://localhost:8000/redoc"
echo "   - Health Check: http://localhost:8000/health"

echo ""
echo "🛑 To stop the container: docker-compose down"