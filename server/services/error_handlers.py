from http import HTTPStatus
from pydantic import ValidationError as PydanticValidationError
from services.exceptions import FitTrackError

def register_error_handlers(app):
    """Register unified JSON error handlers."""
    @app.errorhandler(FitTrackError)
    def handle_fittrack_error(err):
        return err.to_dict(), err.status_code

    @app.errorhandler(PydanticValidationError)
    def handle_pydantic_error(err):
        return {"error": "Validation Error", "details": err.errors()}, HTTPStatus.BAD_REQUEST
