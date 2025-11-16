
set -e
echo "Starting FastAPI dev server..."
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
