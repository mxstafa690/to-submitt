"""Database configuration reader for MySQL credentials."""
import os
import configparser
from urllib.parse import quote_plus


def get_database_uri() -> str:
    """
    Read MySQL credentials from environment variables first, then config.ini.
    
    Environment variables (takes precedence):
        - DATABASE_URL: Full connection string
        - DB_HOST: MySQL host (default: localhost)
        - DB_PORT: MySQL port (default: 3306)
        - DB_USER: MySQL user (default: root)
        - DB_PASSWORD: MySQL password (default: empty)
        - DB_NAME: Database name (default: fittrack)
    
    Falls back to config.ini if environment variables not set.
    
    Returns:
        str: SQLAlchemy database URI in format: mysql+pymysql://user:password@host:port/database
    """
    # Check for full DATABASE_URL environment variable first
    env_uri = os.getenv("DATABASE_URL")
    if env_uri:
        return env_uri
    
    # Check for individual environment variables
    env_host = os.getenv("DB_HOST")
    if env_host:
        # All env vars present, build from them
        host = env_host
        port = os.getenv("DB_PORT", "3306")
        user = os.getenv("DB_USER", "root")
        password = os.getenv("DB_PASSWORD", "")
        database = os.getenv("DB_NAME", "fittrack")
        
        encoded_password = quote_plus(password)
        return f"mysql+pymysql://{user}:{encoded_password}@{host}:{port}/{database}"
    
    # Fall back to config.ini
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'config.ini')
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Configuration file not found at {config_path}. "
            "Please create config.ini with [mysql] section containing: host, port, user, password, database\n"
            "Or set environment variables: DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME"
        )
    
    config.read(config_path)
    
    if 'mysql' not in config:
        raise ValueError("config.ini must contain a [mysql] section")
    
    # Extract MySQL configuration
    mysql_config = config['mysql']
    host = mysql_config.get('host', 'localhost')
    port = mysql_config.get('port', '3306')
    user = mysql_config.get('user', 'root')
    password = mysql_config.get('password', '')
    database = mysql_config.get('database', 'fittrack')
    
    # URL-encode password to handle special characters
    encoded_password = quote_plus(password)
    
    # Build connection string
    database_uri = f"mysql+pymysql://{user}:{encoded_password}@{host}:{port}/{database}"
    
    return database_uri
