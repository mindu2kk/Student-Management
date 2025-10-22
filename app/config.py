import os


class Config:
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        # Example: mysql+pymysql://user:password@localhost:3306/student_mgmt
        "mysql+pymysql://root:password@localhost:3306/student_mgmt",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False


