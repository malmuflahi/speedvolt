import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "speedvolt-dev-secret-key")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "speedvolt-admin")

    database_url = os.environ.get(
        "DATABASE_URL",
        "sqlite:///speedvolt.db"
    )

    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
