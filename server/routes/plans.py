from flask import Blueprint, request, g
from http import HTTPStatus
from schemas.plan_schema import PlanCreate
from services.plan_service import PlanService
from services.exceptions import ForbiddenError
from utils.auth import require_role
from models.admin import Admin


plans_bp = Blueprint("plans", __name__)
plan_service = PlanService()


@plans_bp.route("/plans", methods=["GET"])
@require_role('admin')
def get_plans():
    """Get all subscription plans - ADMIN ONLY."""
    plans = plan_service.list_plans()
    return [p.to_dict() for p in plans], HTTPStatus.OK


@plans_bp.route("/plans/<int:plan_id>", methods=["GET"])
@require_role('admin')
def get_single_plan(plan_id: int):
    """Get specific subscription plan - ADMIN ONLY."""
    plan = plan_service.get_plan(plan_id)
    return plan.to_dict(), HTTPStatus.OK


@plans_bp.route("/plans", methods=["POST"])
@require_role('admin')
def post_plan():
    """Create subscription plan - ADMIN ONLY."""
    payload = PlanCreate.model_validate(request.get_json(force=True))
    plan = plan_service.create_plan(
        name=payload.name,
        type=payload.type,
        price=payload.price,
        valid_days=payload.valid_days,
        max_entries=payload.max_entries,
    )
    result = plan.to_dict()
    result['created_by'] = g.current_user.get_display_name()
    return result, HTTPStatus.CREATED

@plans_bp.route("/plans/<int:plan_id>", methods=["PUT"])
@require_role('admin')
def put_plan(plan_id: int):
    """Update subscription plan - ADMIN ONLY."""
    payload = PlanCreate.model_validate(request.get_json(force=True))
    plan = plan_service.update_plan(
        plan_id=plan_id,
        name=payload.name,
        type=payload.type,
        price=payload.price,
        valid_days=payload.valid_days,
        max_entries=payload.max_entries,
    )
    result = plan.to_dict()
    result['updated_by'] = g.current_user.get_display_name()
    return result, HTTPStatus.OK

@plans_bp.route("/plans/<int:plan_id>", methods=["DELETE"])
@require_role('admin')
def delete_plan(plan_id: int):
    """Delete subscription plan - ADMIN ONLY."""
    plan_service.delete_plan(plan_id)
    return {"deleted": True, "id": plan_id, "deleted_by": g.current_user.get_display_name()}, HTTPStatus.OK
