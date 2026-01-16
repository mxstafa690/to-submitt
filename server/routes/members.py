from flask import Blueprint, request, g
from http import HTTPStatus
from schemas.member_schema import MemberCreate, MemberUpdate
from services.member_service import MemberService
from services.exceptions import ForbiddenError
from utils.auth import login_required, require_role
from models.admin import Admin

members_bp = Blueprint("members", __name__)
member_service = MemberService()

@members_bp.route("/members", methods=["GET"])
@require_role('admin')
def get_members():
    """List all members - Admin only."""
    current_user = g.current_user
    
    members_list = member_service.list_members()
    
    # Include requester info using OOP method
    return {
        'members': members_list,
        'requested_by': current_user.get_display_name()
    }, HTTPStatus.OK.value

@members_bp.route("/members", methods=["POST"])
@require_role('admin')
def post_member():
    """Create member with OOP permission check.
    
    Uses Admin.can_manage_members() to validate admin permissions.
    """
    # USE OOP METHOD: Admin.can_manage_members() checks permissions
    admin = g.current_user
    
    # Store admin display name before service call (to avoid DetachedInstanceError)
    admin_display_name = admin.get_display_name()
    
    if isinstance(admin, Admin) and not admin.can_manage_members():
        raise ForbiddenError(
            f"Admin '{admin_display_name}' does not have permission to manage members. "
            f"Access level: {admin.access_level}"
        )
    
    payload = MemberCreate.model_validate(request.get_json(force=True))
    member_dict = member_service.create_member(
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone,
        national_id=payload.national_id,
        password=payload.password
    )
    
    member_dict['created_by'] = admin_display_name
    return member_dict, HTTPStatus.CREATED

@members_bp.route("/members/<int:member_id>", methods=["GET"])
@require_role('admin')
def get_member_by_id(member_id: int):
    """Get member details - Admin only."""
    current_user = g.current_user
    
    member_dict = member_service.get_member(member_id)
    return member_dict, HTTPStatus.OK

@members_bp.route("/members/<int:member_id>", methods=["PUT"])
@require_role('admin')
def put_member(member_id: int):
    """Update member with OOP permission check.
    
    Uses Admin.can_manage_members() to validate admin permissions.
    """
    # USE OOP METHOD: Admin.can_manage_members() checks permissions
    admin = g.current_user
    if isinstance(admin, Admin) and not admin.can_manage_members():
        raise ForbiddenError(
            f"Admin '{admin.get_display_name()}' does not have permission to manage members. "
            f"Access level: {admin.access_level}"
        )
    
    payload = MemberUpdate.model_validate(request.get_json(force=True))
    # Store admin display name before service call to avoid DetachedInstanceError
    admin_display_name = admin.get_display_name()
    
    member_dict = member_service.update_member(
        member_id=member_id,
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone,
        status=payload.status
    )
    
    member_dict['updated_by'] = admin_display_name
    return member_dict, HTTPStatus.OK

@members_bp.route("/members/<int:member_id>", methods=["DELETE"])
@require_role('admin')
def delete_member(member_id: int):
    """Delete member - Admin only.
    
    Uses Admin.can_manage_members() to validate admin permissions.
    """
    # USE OOP METHOD: Admin.can_manage_members() checks permissions
    admin = g.current_user
    # Store admin display name before service call to avoid DetachedInstanceError
    admin_display_name = admin.get_display_name()
    
    if isinstance(admin, Admin) and not admin.can_manage_members():
        raise ForbiddenError(
            f"Admin '{admin_display_name}' does not have permission to manage members. "
            f"Access level: {admin.access_level}"
        )
    
    member_service.delete_member(member_id)
    return {"deleted": True, "id": member_id, "deleted_by": admin_display_name}, HTTPStatus.OK
