"""
Simple authentication and authorization decorators.
Demonstrates role-based access control (RBAC) without full auth system.
"""
from functools import wraps
from flask import request, g
from services.exceptions import ForbiddenError, NotFoundError
from services.db import get_session
from models.user import User
from models.admin import Admin


def get_current_user():
    """
    Get current user from request header.
    Simple implementation: expects 'X-User-ID' header with user ID.
    In production, this would validate JWT tokens or session cookies.
    
    Returns polymorphic User object (Member/Trainer/Admin) demonstrating OOP inheritance.
    
    Raises:
        ForbiddenError: If X-User-ID is missing or invalid
    """
    user_id_str = request.headers.get('X-User-ID')
    if not user_id_str:
        return None
    
    # Validate X-User-ID is numeric
    try:
        user_id = int(user_id_str)
        if user_id <= 0:
            raise ForbiddenError("X-User-ID must be a positive integer")
    except ValueError:
        raise ForbiddenError("X-User-ID must be numeric")
    
    session = get_session()
    try:
        # Query returns polymorphic object (Member/Trainer/Admin)
        user = session.query(User).filter(User.id == user_id).first()
        return user
    finally:
        session.close()


def login_required(f):
    """
    Decorator to require authentication.
    Usage: @login_required
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            raise ForbiddenError("Authentication required. Provide X-User-ID header.")
        
        if not user.can_login():
            raise ForbiddenError("Account is not active")
        
        g.current_user = user
        return f(*args, **kwargs)
    return decorated_function


def require_role(*allowed_roles):
    """
    Decorator to require specific role(s).
    Usage: @require_role('admin') or @require_role('admin', 'trainer')
    
    Args:
        allowed_roles: One or more role names ('member', 'trainer', 'admin', 'reception')
        
    Note: 'reception' role has limited permissions - typically only check-in operations.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            if not user:
                raise ForbiddenError("Authentication required. Provide X-User-ID header.")
            
            if not user.can_login():
                raise ForbiddenError("Account is not active")
            
            if user.role not in allowed_roles:
                raise ForbiddenError(f"Access denied. Required role: {', '.join(allowed_roles)}")
            
            # Merge user into the request's session to avoid DetachedInstanceError
            if hasattr(g, 'db_session'):
                user = g.db_session.merge(user)
            
            g.current_user = user
            return f(*args, **kwargs)
        return decorated_function
    return decorator
