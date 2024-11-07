from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import conf  # Ensure conf is properly configured
from urllib.parse import quote_plus

# Build database URL with credentials
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{conf.user}:{quote_plus(conf.password)}@{conf.host}:{conf.port}/{conf.database}?charset=utf8mb4"

# Create engine and session local
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the models
Base = declarative_base()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
