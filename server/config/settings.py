"""
⚠️ OBSOLETE FILE - NOT IN USE

This file is not used in the current implementation.
Database configuration is now centralized in config.ini at project root.

For MySQL configuration, see:
- config.ini (project root) - Database credentials
- config/db_config.py - Configuration reader
- CONFIG_GUIDE.md - Comprehensive documentation

Configuration is read via: from config.db_config import get_database_uri
"""

# This file is kept for reference only
# The application uses config.ini for database configuration
# via the config/db_config.py module


def get_config():
    """Get configuration based on environment."""
    env = os.getenv("FLASK_ENV", "development")
    return config.get(env, config["default"])
