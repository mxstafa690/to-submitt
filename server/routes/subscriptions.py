from flask import Blueprint, request, g
from http import HTTPStatus
from schemas.subscription_schema import SubscriptionCreate, FreezeRequest
from services.subscription_service import SubscriptionService
from services.exceptions import ForbiddenError
from utils.auth import login_required, require_role


subscriptions_bp = Blueprint("subscriptions", __name__)
subscription_service = SubscriptionService()


@subscriptions_bp.route("/members/<int:member_id>/subscriptions", methods=["GET"])
@login_required
def get_member_subscriptions(member_id: int):
    """Get member subscriptions - Admin, Trainer, or self only."""
    current_user = g.current_user
    
    # Admin and trainer can view any member, members can only view themselves
    if current_user.role not in ['admin', 'trainer'] and current_user.id != member_id:
        raise ForbiddenError("You can only view your own subscriptions")
    
    subs = subscription_service.list_member_subscriptions(member_id)
    return [s.to_dict() for s in subs], HTTPStatus.OK


@subscriptions_bp.route("/members/<int:member_id>/subscriptions", methods=["POST"])
@require_role('admin', 'trainer')
def post_member_subscription(member_id: int):
    payload = SubscriptionCreate.model_validate(request.get_json(force=True))
    sub = subscription_service.create_subscription(member_id=member_id, plan_id=payload.plan_id, start_date_value=payload.start_date)
    return sub.to_dict(), HTTPStatus.CREATED


@subscriptions_bp.route("/subscriptions/<int:subscription_id>", methods=["GET"])
@login_required
def get_single_subscription(subscription_id: int):
    """Get subscription details - Admin/Trainer can view any, members only their own."""
    current_user = g.current_user
    sub = subscription_service.get_subscription(subscription_id)
    
    # Admin and trainer can view any subscription
    if current_user.role in ['trainer', 'admin']:
        return sub.to_dict(), HTTPStatus.OK
    
    # Members can only view their own subscriptions
    if current_user.role == 'member' and sub.member_id == current_user.id:
        return sub.to_dict(), HTTPStatus.OK
    
    raise ForbiddenError("You can only view your own subscriptions")


@subscriptions_bp.route("/subscriptions/<int:subscription_id>/freeze", methods=["PATCH"])
@require_role('trainer', 'admin')
def patch_freeze(subscription_id: int):
    payload = FreezeRequest.model_validate(request.get_json(force=True))
    sub = subscription_service.freeze_subscription(subscription_id, payload.days)
    return sub.to_dict(), HTTPStatus.OK


@subscriptions_bp.route("/subscriptions/<int:subscription_id>/unfreeze", methods=["PATCH"])
@require_role('trainer', 'admin')
def patch_unfreeze(subscription_id: int):
    sub = subscription_service.unfreeze_subscription(subscription_id)
    return sub.to_dict(), HTTPStatus.OK


@subscriptions_bp.route("/subscriptions/<int:subscription_id>", methods=["DELETE"])
@require_role('trainer', 'admin')
def delete_subscription(subscription_id: int):
    """Delete a subscription - Trainer and Admin only."""
    subscription_service.delete_subscription(subscription_id)
    return {"deleted": True, "id": subscription_id}, HTTPStatus.OK


@subscriptions_bp.route("/members/<int:member_id>/subscription-status", methods=["GET"])
@login_required
def get_subscription_status(member_id: int):
    """Get subscription status - Admin/Trainer can view any, members only their own."""
    current_user = g.current_user
    
    # Admin and trainer can view any member's status
    if current_user.role in ['trainer', 'admin']:
        status = subscription_service.subscription_status_for_member(member_id)
        return status, HTTPStatus.OK
    
    # Members can only view their own status
    if current_user.role == 'member' and current_user.id == member_id:
        status = subscription_service.subscription_status_for_member(member_id)
        return status, HTTPStatus.OK
    
    raise ForbiddenError("You can only view your own subscription status")
