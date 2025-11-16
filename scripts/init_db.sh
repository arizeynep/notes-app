
set -e
echo "Initializing SQLite database..."

./venv/bin/python - <<'PY'
from app.db.database import Base, engine
from app.db.models import Note
Base.metadata.create_all(bind=engine)
print("Database initialized.")
PY
