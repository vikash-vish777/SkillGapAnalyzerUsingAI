import os
from datetime import timedelta
from dotenv import load_dotenv
from sqlalchemy.engine import URL


# Project base directory
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

# Load environment variables
load_dotenv(os.path.join(BASE_DIR, ".env"))
load_dotenv()


class Config:

    # Security settings
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key-skill-gap-change-in-prod"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "dev-jwt-secret-key-change-in-prod"
    )

    jwt_minutes = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", 1440)
    )

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=jwt_minutes)

    # CORS settings
    raw_origins = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173"
    )

    CORS_ORIGINS = [
        origin.strip()
        for origin in raw_origins.split(",")
        if origin.strip()
    ]

    # File upload settings
    MAX_CONTENT_LENGTH = (
        int(os.getenv("MAX_CONTENT_LENGTH_MB", 5)) * 1024 * 1024
    )

    ALLOWED_EXTENSIONS = {"pdf", "docx"}

    # SQLite fallback
    USE_SQLITE_FALLBACK = os.getenv(
        "USE_SQLITE_FALLBACK", "false"
    ).lower() in ("true", "1", "yes")

    # Aiven MySQL database settings
    DB_USER = os.getenv("DB_USER", "avnadmin")

    DB_PASSWORD = os.getenv("DB_PASSWORD", "")

    DB_HOST = os.getenv(
        "DB_HOST",
        "mysql-1562a1f8-vikash13306-22af.f.aivencloud.com"
    )

    DB_PORT = os.getenv("DB_PORT", "12526")

    DB_NAME = os.getenv("DB_NAME", "skill_gap_db")

    # Database connection
    if USE_SQLITE_FALLBACK:

        sqlite_path = os.path.join(
            BASE_DIR,
            "instance",
            "skill_gap_local.db"
        )

        os.makedirs(
            os.path.dirname(sqlite_path),
            exist_ok=True
        )

        SQLALCHEMY_DATABASE_URI = f"sqlite:///{sqlite_path}"

    else:

        SQLALCHEMY_DATABASE_URI = URL.create(
            drivername="mysql+pymysql",
            username=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=int(DB_PORT),
            database=DB_NAME,
            query={"charset": "utf8mb4"}
        )

    # SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 280,
        "pool_pre_ping": True,
    }

    # Aiven SSL settings
    DB_SSL_CA = os.getenv("DB_SSL_CA")

    if not USE_SQLITE_FALLBACK:

        if not DB_SSL_CA:
            raise RuntimeError(
                "DB_SSL_CA is required in production"
            )

        SQLALCHEMY_ENGINE_OPTIONS["connect_args"] = {
            "ssl": {
                "ca": DB_SSL_CA
            }
        }

    # Rate limiting
    RATELIMIT_ENABLED = True

    RATELIMIT_DEFAULT = "200 per day;50 per hour"

    RATELIMIT_STRATEGY = "fixed-window"