from flask import Blueprint, request, g
from http import HTTPStatus

from services.workout_plan_service import WorkoutPlanService
from services.exceptions import BadRequestError
from utils.auth import login_required, require_role

workout_plans_bp = Blueprint("workout_plans_bp", __name__)
workout_plan_service = WorkoutPlanService()


@workout_plans_bp.route("/workout-plans", methods=["POST"])
@require_role('trainer', 'admin')
def post_workout_plan():
    """Create workout plan with OOP permission check.
    
    Uses Trainer.can_manage_workout_plans() to validate trainer permissions.
    Admins can bypass trainer-specific checks.
    """
    data = request.get_json(force=True) or {}
    
    # Pass trainer_id if current user is a trainer (for OOP permission check)
    trainer_id = g.current_user.id if g.current_user.role == 'trainer' else None
    created = workout_plan_service.create_workout_plan(data, trainer_id=trainer_id)
    
    # Include creator display name in response
    result = created.to_dict()
    result['created_by'] = g.current_user.get_display_name()
    return result, HTTPStatus.CREATED

@workout_plans_bp.route("/workout-plans/<int:plan_id>", methods=["GET"])
@login_required
def get_workout_plan(plan_id: int):
    """Get specific workout plan - Trainer, Admin, or member assigned to plan."""
    current_user = g.current_user
    plan = workout_plan_service.get_workout_plan(plan_id)
    
    # Trainer and admin can view any plan
    if current_user.role in ['trainer', 'admin']:
        return plan.to_dict(), HTTPStatus.OK
    
    # Members can view only their own plans
    if current_user.role == 'member' and plan.member_id == current_user.id:
        return plan.to_dict(), HTTPStatus.OK
    
    raise ForbiddenError("You don't have permission to view this workout plan")


@workout_plans_bp.route("/members/<int:member_id>/workout-plans", methods=["GET"])
@login_required
def get_member_workout_plans(member_id: int):
    plans = workout_plan_service.list_member_workout_plans(member_id)
    return [p.to_dict() for p in plans], HTTPStatus.OK


@workout_plans_bp.route("/members/<int:member_id>/workout-plans/active", methods=["GET"])
def get_member_active_plan(member_id: int):
    result = workout_plan_service.get_member_active_workout_plan(member_id)
    if result is None:
        return None, HTTPStatus.OK
    plan, items = result
    return {"plan": plan.to_dict(), "items": [i.to_dict() for i in items]}, HTTPStatus.OK


@workout_plans_bp.route("/workout-plans/<int:plan_id>/active", methods=["PATCH"])
def patch_plan_active(plan_id: int):
    data = request.get_json(force=True) or {}
    if "is_active" not in data:
        raise BadRequestError("Missing field: is_active")
    plan = workout_plan_service.set_workout_plan_active(plan_id, bool(data["is_active"]))
    return plan.to_dict(), HTTPStatus.OK


@workout_plans_bp.route("/workout-plans/<int:plan_id>/items", methods=["GET"])
def get_plan_items(plan_id: int):
    items = workout_plan_service.get_workout_plan_items(plan_id)
    return [i.to_dict() for i in items], HTTPStatus.OK


@workout_plans_bp.route("/workout-items/<int:item_id>", methods=["GET"])
def get_item(item_id: int):
    item = workout_plan_service.get_workout_item(item_id)
    return item.to_dict(), HTTPStatus.OK


@workout_plans_bp.route("/workout-items/<int:item_id>", methods=["PATCH"])
@require_role('trainer', 'admin')
def patch_item(item_id: int):
    data = request.get_json(force=True) or {}
    if not data:
        raise BadRequestError("No fields to update")
    item = workout_plan_service.update_workout_item(item_id, data)
    return item.to_dict(), HTTPStatus.OK


@workout_plans_bp.route("/workout-items/<int:item_id>", methods=["DELETE"])
@require_role('trainer', 'admin')
def delete_item(item_id: int):
    workout_plan_service.delete_workout_item(item_id)
    return {"deleted": True, "id": item_id}, HTTPStatus.OK
