import os
from app import create_app

app = create_app(os.getenv("FLASK_ENV", "development"))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    print(f"[*] Starting Skill Gap Analyzer API on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
