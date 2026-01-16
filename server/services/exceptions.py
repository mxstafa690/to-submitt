class FitTrackError(Exception):
    status_code = 400

    def __init__(self, message=""):
        super().__init__(message)
        self.message = message

    def to_dict(self):
        return {"error": self.__class__.__name__, "message": self.message}


class NotFoundError(FitTrackError):
    status_code = 404


class BadRequestError(FitTrackError):
    status_code = 400


class DuplicateError(FitTrackError):
    status_code = 409


class ForbiddenError(FitTrackError):
    status_code = 403
