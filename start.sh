#!/usr/bin/env bash
set -e

PROJECT_DIR="$HOME/Zeynep/projects/notes-app"

cd "$PROJECT_DIR"

# Create venv if missing
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install deps if missing
python3 -m pip install --upgrade uv
uv pip install -r requirements.txt

# Init DB
./scripts/init_db.sh

# Run dev servers
./scripts/run_dev.sh
