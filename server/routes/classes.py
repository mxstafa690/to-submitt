from flask import Blueprint, request, g
from http import HTTPStatus
from schemas.class_schema import ClassCreate
from schemas.session_schema import SessionCreate
from services.class_service import ClassService
from services.session_service import SessionService
from services.waiting_list_service import WaitingListService
from services.exceptions import ForbiddenError
from utils.auth import require_role, login_required


classes_bp = Blueprint("classes", __name__)
class_service = ClassService()
session_service = SessionService()
waiting_list_service = WaitingListService()


@classes_bp.route("/classes", methods=["GET"])
@login_required
def get_classes():
    """Get classes - All classes for admin/trainer, only registered classes for members."""
    current_user = g.current_user
    
    # Admin and trainer can view all classes
    if current_user.role in ['trainer', 'admin']:
        classes = class_service.list_classes()
        return [c.to_dict(include_stats=True) for c in classes], HTTPStatus.OK
    
    # Members can only view classes they are registered in
    if current_user.role == 'member':
        all_classes = class_service.list_classes()
        member_classes = []
        for cls in all_classes:
            participants = session_service.get_participants(cls.id)
            participant_ids = [p.id for p in participants]
            if current_user.id in participant_ids:
                member_classes.append(cls)
        return [c.to_dict(include_stats=True) for c in member_classes], HTTPStatus.OK
    
    raise ForbiddenError("You don't have permission to view classes")


@classes_bp.route("/classes", methods=["POST"])
@require_role('trainer', 'admin')
def post_class():
    """Create gym class with OOP permission check.
    
    Uses Trainer.can_create_classes() to validate trainer permissions.
    Admins can bypass trainer-specific checks.
    """
    payload = ClassCreate.model_validate(request.get_json(force=True))
    
    # Pass trainer_id if current user is a trainer (for OOP permission check)
    trainer_id = g.current_user.id if g.current_user.role == 'trainer' else None
    
    gym_class = class_service.create_class(
        title=payload.title,
        instructor=payload.instructor,
        start_time=payload.start_time,
        duration_minutes=payload.duration_minutes,
        capacity=payload.capacity,
        trainer_id=trainer_id
    )
    
    # Include creator display name in response
    result = gym_class.to_dict(include_stats=True)
    result['created_by'] = g.current_user.get_display_name()
    return result, HTTPStatus.CREATED


@classes_bp.route("/classes/<int:class_id>", methods=["GET"])
@login_required
def get_one_class(class_id: int):
    """Get class details - Admin/Trainer can view any, members only if registered."""
    current_user = g.current_user
    gym_class = class_service.get_class(class_id)
    
    # Admin and trainer can view any class
    if current_user.role in ['trainer', 'admin']:
        return gym_class.to_dict(include_stats=True), HTTPStatus.OK
    
    # Members can only view classes they are registered in
    if current_user.role == 'member':
        participants = session_service.get_participants(class_id)
        participant_ids = [p.id for p in participants]
        if current_user.id not in participant_ids:
            raise ForbiddenError("You are not registered in this class")
        return gym_class.to_dict(include_stats=True), HTTPStatus.OK
    
    raise ForbiddenError("You don't have permission to view this class")

@classes_bp.route("/classes/<int:class_id>", methods=["PUT"])
@require_role('trainer', 'admin')
def put_class(class_id: int):
    """Update gym class - Trainer and Admin only."""
    payload = ClassCreate.model_validate(request.get_json(force=True))
    gym_class = class_service.update_class(
        class_id=class_id,
        title=payload.title,
        instructor=payload.instructor,
        start_time=payload.start_time,
        duration_minutes=payload.duration_minutes,
        capacity=payload.capacity,
    )
    result = gym_class.to_dict(include_stats=True)
    result['updated_by'] = g.current_user.get_display_name()
    return result, HTTPStatus.OK

@classes_bp.route("/classes/<int:class_id>", methods=["DELETE"])
@require_role('trainer', 'admin')
def delete_class(class_id: int):
    """Delete gym class - Trainer and Admin only."""
    class_service.delete_class(class_id)
    return {"deleted": True, "id": class_id, "deleted_by": g.current_user.get_display_name()}, HTTPStatus.OK


@classes_bp.route("/classes/<int:class_id>/sessions", methods=["POST"])
@require_role('trainer', 'admin')
def post_session(class_id: int):
    payload = SessionCreate.model_validate(request.get_json(force=True))
    s = session_service.register_member_to_class(class_id=class_id, member_id=payload.member_id)
    return s.to_dict(), HTTPStatus.CREATED

@classes_bp.route("/classes/<int:class_id>/sessions", methods=["GET"])
@login_required
def get_sessions(class_id: int):
    """Get sessions for a class - Trainer, Admin, or members of the class only."""
    current_user = g.current_user
    
    # Trainer and admin can view any class sessions
    if current_user.role in ['trainer', 'admin']:
        sessions = session_service.get_class_sessions(class_id=class_id)
        return [s.to_dict() for s in sessions], HTTPStatus.OK
    
    # Members can view sessions only if they are registered in the class
    if current_user.role == 'member':
        members = session_service.get_participants(class_id=class_id)
        member_ids = [m.id for m in members]
        if current_user.id not in member_ids:
            raise ForbiddenError("You are not registered in this class")
        sessions = session_service.get_class_sessions(class_id=class_id)
        return [s.to_dict() for s in sessions], HTTPStatus.OK
    
    raise ForbiddenError("You don't have permission to view class sessions")


@classes_bp.route("/classes/<int:class_id>/sessions/<int:member_id>", methods=["DELETE"])
@require_role('trainer', 'admin')
def delete_session(class_id: int, member_id: int):
    s = session_service.cancel_registration(class_id=class_id, member_id=member_id)
    return s.to_dict(), HTTPStatus.OK


@classes_bp.route("/classes/<int:class_id>/participants", methods=["GET"])
@login_required
def get_class_participants(class_id: int):
    """Get participants in a class - Trainer, Admin, or members of the class only."""
    current_user = g.current_user
    
    # Trainer and admin can view any class participants
    if current_user.role in ['trainer', 'admin']:
        members = session_service.get_participants(class_id=class_id)
        return [m.to_dict() for m in members], HTTPStatus.OK
    
    # Members can view participants only if they are registered in the class
    if current_user.role == 'member':
        members = session_service.get_participants(class_id=class_id)
        # Check if current member is in the class
        member_ids = [m.id for m in members]
        if current_user.id not in member_ids:
            raise ForbiddenError("You are not registered in this class")
        return [m.to_dict() for m in members], HTTPStatus.OK
    
    raise ForbiddenError("You don't have permission to view class participants")


@classes_bp.route("/classes/<int:class_id>/stats", methods=["GET"])
@login_required
def get_stats(class_id: int):
    """Get class statistics - Trainer, Admin, or members of the class only."""
    current_user = g.current_user
    
    # Trainer and admin can view any class stats
    if current_user.role in ['trainer', 'admin']:
        return session_service.get_class_stats(class_id=class_id), HTTPStatus.OK
    
    # Members can view stats only if they are registered in the class
    if current_user.role == 'member':
        members = session_service.get_participants(class_id=class_id)
        # Check if current member is in the class
        member_ids = [m.id for m in members]
        if current_user.id not in member_ids:
            raise ForbiddenError("You are not registered in this class")
        return session_service.get_class_stats(class_id=class_id), HTTPStatus.OK
    
    raise ForbiddenError("You don't have permission to view class stats")


@classes_bp.route("/classes/<int:class_id>/waitlist", methods=["GET"])
def get_waitlist(class_id: int):
    """Get waiting list for a class."""
    entries = waiting_list_service.get_waitlist(class_id)
    return [e.to_dict() for e in entries], HTTPStatus.OK


@classes_bp.route("/classes/<int:class_id>/waitlist", methods=["POST"])
def post_waitlist(class_id: int):
    """Add member to waiting list."""
    payload = SessionCreate.model_validate(request.get_json(force=True))
    entry = waiting_list_service.add_to_waitlist(class_id=class_id, member_id=payload.member_id)
    return entry.to_dict(), HTTPStatus.CREATED


@classes_bp.route("/classes/<int:class_id>/waitlist/<int:member_id>", methods=["DELETE"])
def delete_waitlist(class_id: int, member_id: int):
    """Remove member from waiting list."""
    waiting_list_service.remove_from_waitlist(class_id=class_id, member_id=member_id)
    return {"message": "Removed from waiting list"}, HTTPStatus.OK
