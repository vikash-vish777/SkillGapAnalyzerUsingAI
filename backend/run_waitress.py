"""Production WSGI Server for Windows and Cross-Platform Environments using Waitress."""
import os
import sys

# Ensure backend root is on Python module search path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from waitress import serve
from wsgi import app

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    threads = int(os.getenv("WAITRESS_THREADS", 8))

    print(f"============================================================")
    print(f"Starting Skill Gap Analyzer API (Production Mode via Waitress)")
    print(f"Listening on: http://{host}:{port}")
    print(f"Worker Threads: {threads}")
    print(f"============================================================")

    serve(
        app,
        host=host,
        port=port,
        threads=threads,
        connection_limit=200,
        channel_timeout=60,
    )

