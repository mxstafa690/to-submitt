from flask import Flask, g
from flask_cors import CORS

from config.db_config import get_database_uri
from services import db
from services.error_handlers import register_error_handlers

from routes.health import health_bp
from routes.members import members_bp
from routes.plans import plans_bp
from routes.subscriptions import subscriptions_bp
from routes.payments import payments_bp
from routes.checkins import checkins_bp
from routes.workout_plans import workout_plans_bp
from routes.classes import classes_bp


def create_app() -> Flask:
    app = Flask(__name__)

    # Enable CORS for all routes (allows frontend on port 8000 to access backend)
    CORS(app)

    # DB config - MySQL with PyMySQL (read from config.ini)
    database_uri = get_database_uri()

    # Initialize database
    db.init_db(database_uri)

    # Create tables
    db.create_all_tables()

    # Attach database session to request context
    @app.before_request
    def attach_session():
        """Attach a database session to the Flask g object for this request."""
        if db.SessionLocal is None:
            raise RuntimeError("Database not initialized. SessionLocal is None.")
        g.db_session = db.SessionLocal()

    # Clean up session after each request
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """Close database session at end of request."""
        session = g.pop('db_session', None)
        if session is not None:
            session.close()
        db.close_session()

    # error handlers (FitTrackError וכו')
    register_error_handlers(app)

    # Register blueprints (כל ה-API תחת /api)
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(members_bp, url_prefix="/api")
    app.register_blueprint(plans_bp, url_prefix="/api")
    app.register_blueprint(subscriptions_bp, url_prefix="/api")
    app.register_blueprint(payments_bp, url_prefix="/api")
    app.register_blueprint(checkins_bp, url_prefix="/api")
    app.register_blueprint(workout_plans_bp, url_prefix="/api")
    app.register_blueprint(classes_bp, url_prefix="/api")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
