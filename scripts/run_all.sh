#!/bin/bash

# All-in-One Launcher - Start Backend + Frontend

PROJECT_DIR="/Users/chandangowdatk/Development/Market Analyst Agent/Market_Analyst_Agent"

echo "============================================"
echo "🚀 Market Analyst Agent - Full Stack Launch"
echo "============================================"
echo ""

cd "$PROJECT_DIR" || exit 1

# Check .env file
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create .env file with your API keys first."
    echo "See START_HERE.md for instructions."
    exit 1
fi

echo "✅ Activating virtual environment..."
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

echo "✅ Checking backend health..."

# Start backend in background
echo "🔧 Starting backend server..."
python src/main.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait for backend to be ready
echo "⏳ Waiting for backend to start..."
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "✅ Backend is running!"
else
    echo "⚠️  Backend might still be starting..."
fi

# Start frontend
echo "🌐 Starting frontend server..."
cd frontend
python3 -m http.server 3000 > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo "   Frontend PID: $FRONTEND_PID"
echo ""
echo "============================================"
echo "✅ All systems running!"
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
echo "🌐 Opening frontend in browser..."
sleep 2

# Open browser
if command -v open &> /dev/null; then
    open http://localhost:3000
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3000
else
    echo "Please open: http://localhost:3000"
fi

echo ""
echo "⚠️  To stop all services:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo "   or press Ctrl+C (may need to kill manually)"
echo ""

# Save PIDs to file for easy cleanup
echo "$BACKEND_PID" > .backend.pid
echo "$FRONTEND_PID" > .frontend.pid

echo "Press Ctrl+C to view instructions for stopping..."
echo ""

# Keep script running
wait

