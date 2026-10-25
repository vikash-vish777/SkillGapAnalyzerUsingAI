#!/bin/bash
set -e

echo "=== Skill Gap Analyzer Backend Service Starting ==="

# Wait for database if DB_HOST is set
if [ -n "$DB_HOST" ] && [ "$USE_SQLITE_FALLBACK" != "true" ]; then
    echo "Waiting for database at $DB_HOST:${DB_PORT:-3306}..."
    python - <<END
import socket
import time
import os
import sys

host = os.getenv("DB_HOST", "localhost")
port = int(os.getenv("DB_PORT", 3306))
timeout = 60
start = time.time()

while True:
    try:
        with socket.create_connection((host, port), timeout=2):
            print(f"Successfully reached database at {host}:{port}")
            sys.exit(0)
    except Exception as exc:
        if time.time() - start > timeout:
            print(f"Database connection timed out after {timeout} seconds: {exc}")
            sys.exit(1)
        print("Database not ready yet, sleeping 2 seconds...")
        time.sleep(2)
END
fi

# Run database migrations
echo "Applying database schema migrations..."
flask db upgrade || echo "Migrations already applied or skipped."

# Seed initial job roles, canonical skills, and verified resources if needed
echo "Seeding initial reference data..."
python - <<END
import os
import sys

try:
    if os.path.exists("database/seed_data.py"):
        import subprocess
        subprocess.run([sys.executable, "database/seed_data.py"], check=True)
    elif os.path.exists("../database/seed_data.py"):
        import subprocess
        subprocess.run([sys.executable, "../database/seed_data.py"], check=True)
except Exception as exc:
    print(f"Notice: Seed check completed: {exc}")
END

echo "Starting Gunicorn WSGI server..."
exec gunicorn \
    --bind 0.0.0.0:${PORT:-5000} \
    --workers ${GUNICORN_WORKERS:-4} \
    --threads ${GUNICORN_THREADS:-2} \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    "wsgi:app"

