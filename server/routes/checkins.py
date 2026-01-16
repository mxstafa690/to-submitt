from flask import Blueprint, request, g
from http import HTTPStatus

from services.checkin_service import CheckinService
from services.exceptions import FitTrackError, ForbiddenError
from utils.auth import login_required, require_role

checkins_bp = Blueprint("checkins", __name__)
checkin_service = CheckinService()


@checkins_bp.route("/checkins", methods=["POST"])
@require_role('member')
def post_checkin():
    """Check-in member to gym.
    
    Only MEMBER role can create check-ins (self-service check-in).
    Reuses existing checkin_service.checkin_member() business logic.
    """
    data = request.get_json(force=True) or {}
    member_id = data.get("member_id")

    # checks if the member_id is provided
    if not member_id:
        raise FitTrackError("member_id is required")

    checkin = checkin_service.checkin_member(int(member_id))
    return checkin.to_dict(), HTTPStatus.CREATED


@checkins_bp.route("/checkins", methods=["GET"])
@require_role('reception')
def get_checkins():
    """Get checkins - RECEPTION only.
    
    Only RECEPTION role can view check-in records.
    This allows front desk staff to monitor gym attendance.
    """
    member_id = request.args.get("member_id", type=int)
    items = checkin_service.list_checkins(member_id=member_id)
    return [c.to_dict() for c in items], HTTPStatus.OK

@checkins_bp.route("/checkins/<int:checkin_id>", methods=["GET"])
@require_role('reception', 'admin')
def get_checkin_by_id(checkin_id: int):
    """Get specific check-in - Reception and Admin only."""
    checkin = checkin_service.get_checkin(checkin_id)
    return checkin.to_dict(), HTTPStatus.OK

@checkins_bp.route("/checkins/<int:checkin_id>", methods=["PUT"])
@require_role('reception', 'admin')
def put_checkin(checkin_id: int):
    """Update check-in result - Reception and Admin only."""
    data = request.get_json(force=True) or {}
    result_status = data.get("result")
    reason = data.get("reason")
    
    if not result_status:
        raise FitTrackError("result field is required (approved/denied)")
    
    checkin = checkin_service.update_checkin(checkin_id, result_status, reason)
    return checkin.to_dict(), HTTPStatus.OK

@checkins_bp.route("/checkins/<int:checkin_id>", methods=["DELETE"])
@require_role('admin')
def delete_checkin(checkin_id: int):
    """Delete check-in - Admin only."""
    checkin_service.delete_checkin(checkin_id)
    return {"deleted": True, "id": checkin_id}, HTTPStatus.OK
