set -e # Stop the script if any command fails

# Trap to kill both processes on script exit
cleanup() {
  echo "Stopping servers..."
  # Kill both backend and frontend processes if they are running
  kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
  exit 0
}
trap cleanup SIGINT SIGTERM

echo "Starting FastAPI dev server on http://0.0.0.0:8000..."
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo "Starting Vite frontend dev server on http://localhost:5173..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "Both servers running. Press Ctrl+C to stop."
wait
