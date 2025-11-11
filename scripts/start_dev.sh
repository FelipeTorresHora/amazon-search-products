#!/bin/bash
# Start development environment

set -e

echo "🚀 Starting Amazon Search Products - Development Environment"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Start services
echo "📦 Starting Docker services..."
docker-compose up -d db redis

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 5

# Initialize database
echo "🗄️  Initializing database..."
python3 scripts/init_db.py

# Start backend
echo "🔧 Starting backend..."
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start frontend
echo "🎨 Starting frontend..."
cd ../frontend
streamlit run app.py --server.port 8501 &
FRONTEND_PID=$!

# Start Celery worker
echo "⚙️  Starting Celery worker..."
cd ../backend
celery -A app.tasks.celery_app worker --loglevel=info &
CELERY_PID=$!

echo ""
echo "✅ Development environment started!"
echo ""
echo "📍 Services:"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/api/v1/docs"
echo "   Frontend: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID $CELERY_PID; docker-compose down" INT
wait
