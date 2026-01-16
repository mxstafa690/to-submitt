"""Database configuration using plain SQLAlchemy.

Database credentials are read from config.ini at project root via config.db_config module.
This module handles SQLAlchemy engine initialization and session management.
"""
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

"""
this is to create tables as classes
"""
# Create declarative base for models
Base = declarative_base()

# Global engine and session factory (will be initialized in init_db)
engine = None
SessionLocal = None


def init_db(database_uri: str):
    """Initialize database engine and session factory.
    
    Args:
        database_uri: SQLAlchemy database URI (from config.db_config.get_database_uri())
    """
    global engine, SessionLocal
    
    try:
        engine = create_engine(
            database_uri,
            echo=False,
            pool_pre_ping=True,
            pool_recycle=3600,  # Recycle connections after 1 hour
            pool_size=10,  # Connection pool size
            max_overflow=20  # Max connections beyond pool_size
        )
        
        # Create scoped session factory  
        SessionLocal = scoped_session(sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        ))
        
        # Verify SessionLocal is properly set
        if SessionLocal is None:
            raise RuntimeError("SessionLocal was not properly initialized")
        
        print(f"Database initialized successfully: {database_uri.split('@')[1] if '@' in database_uri else 'database'}")
    except Exception as e:
        print(f"ERROR: Failed to initialize database: {e}")
        raise


def create_all_tables():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)


def get_session():
    """Get a new database session.
    
    Returns:
        SQLAlchemy session
    """
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return SessionLocal()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations.
    
    Usage:
        with session_scope() as session:
            session.add(obj)
    """
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def close_session():
    """Close the current scoped session."""
    if SessionLocal:
        SessionLocal.remove()
