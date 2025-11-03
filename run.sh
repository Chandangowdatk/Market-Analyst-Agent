#!/bin/bash

# Market Analyst Agent - Full Stack Launcher
# Starts both backend (FastAPI) and frontend (React)

PROJECT_DIR="/Users/chandangowdatk/Development/Market Analyst Agent/Market_Analyst_Agent"

echo "============================================"
echo "🚀 Market Analyst Agent - Starting Services"
echo "============================================"
echo ""

cd "$PROJECT_DIR" || exit 1

# Check .env file
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo ""
    echo "Create .env file with:"
    echo "  GOOGLE_API_KEY=your_key"
    echo "  OPENAI_API_KEY=your_key"
    echo "  PINECONE_API_KEY=your_key"
    exit 1
fi

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found!"
    echo "Create it with: python3 -m venv venv"
    exit 1
fi

# Activate venv
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Set Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "============================================"
    echo "🛑 Stopping services..."
    echo "============================================"
    
    if [ ! -z "$BACKEND_PID" ]; then
        echo "Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        echo "Stopping frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID 2>/dev/null
    fi
    
    # Clean up PID files
    rm -f .backend.pid .frontend.pid
    
    echo "✅ Services stopped"
    exit 0
}

# Trap Ctrl+C and cleanup
trap cleanup SIGINT SIGTERM

# Start backend
echo "🔧 Starting backend server..."
python src/main.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"
echo $BACKEND_PID > .backend.pid

# Wait for backend to be ready
echo "⏳ Waiting for backend to start..."
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "✅ Backend is running on http://localhost:8000"
else
    echo "⚠️  Backend might still be starting... (check backend.log)"
fi

# Check if node_modules exists for frontend
if [ ! -d "frontend/node_modules" ]; then
    echo ""
    echo "⚠️  Frontend dependencies not installed!"
    echo "Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Start frontend
echo "🌐 Starting frontend server..."
cd frontend

# Set environment variable to prevent npm start from opening browser automatically
export BROWSER=none

# Start React app in background
npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo "   Frontend PID: $FRONTEND_PID"
echo $FRONTEND_PID > .frontend.pid

# Wait a bit for frontend to start
echo "⏳ Waiting for frontend to start..."
sleep 5

echo ""
echo "============================================"
echo "✅ All services running!"
echo "============================================"
echo ""
echo "📍 URLs:"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:3000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📝 Logs:"
echo "   Backend:  tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo ""
echo "🛑 To stop: Press Ctrl+C"
echo ""

# Open browser after short delay
sleep 3
if command -v open &> /dev/null; then
    echo "🌐 Opening frontend in browser..."
    open http://localhost:3000
elif command -v xdg-open &> /dev/null; then
    echo "🌐 Opening frontend in browser..."
    xdg-open http://localhost:3000
fi

echo ""
echo "Press Ctrl+C to stop all services..."
echo ""

# Wait for processes (keep script running)
while kill -0 $BACKEND_PID 2>/dev/null || kill -0 $FRONTEND_PID 2>/dev/null; do
    sleep 1
done

# If we get here, both processes have exited
cleanup
