from flask import Blueprint, request, g
from http import HTTPStatus

from schemas.payment_schema import PaymentCreate, PaymentStatusUpdate
from services.payment_service import PaymentService
from services.exceptions import ForbiddenError
from utils.auth import require_role, login_required
from models.admin import Admin

payments_bp = Blueprint("payments", __name__)
payment_service = PaymentService()


@payments_bp.route("/payments", methods=["GET"])
@login_required
def get_payments():
    """List all payments - Admin only."""
    current_user = g.current_user
    if current_user.role != 'admin':
        raise ForbiddenError("Only admins can view payments")
    
    subscription_id = request.args.get("subscription_id", type=int)
    payments = payment_service.list_payments(subscription_id=subscription_id)
    return [p.to_dict() for p in payments], HTTPStatus.OK


@payments_bp.route("/payments", methods=["POST"])
@require_role('admin')
def post_payment():
    """Create payment with OOP permission check.
    
    Uses Admin.can_manage_finances() to validate admin permissions.
    """
    # USE OOP METHOD: Admin.can_manage_finances() checks permissions
    admin = g.current_user
    if isinstance(admin, Admin) and not admin.can_manage_finances():
        raise ForbiddenError(
            f"Admin '{admin.get_display_name()}' does not have permission to manage finances. "
            f"Required: 'full' access level, Current: '{admin.access_level}'"
        )
    
    payload = PaymentCreate.model_validate(request.get_json(force=True))
    payment = payment_service.create_payment(
        subscription_id=payload.subscription_id,
        amount=payload.amount,
        reference=payload.reference,
    )
    
    result = payment.to_dict()
    result['created_by'] = admin.get_display_name()
    return result, HTTPStatus.CREATED


@payments_bp.route("/payments/<int:payment_id>", methods=["GET"])
@login_required
def get_payment_by_id(payment_id: int):
    """Get payment details - Admin only."""
    current_user = g.current_user
    if current_user.role != 'admin':
        raise ForbiddenError("Only admins can view payment details")
    
    payment = payment_service.get_payment(payment_id)
    return payment.to_dict(), HTTPStatus.OK


@payments_bp.route("/payments/<int:payment_id>/status", methods=["PUT"])
@require_role('admin')
def put_payment_status(payment_id: int):
    """Update payment status with OOP permission check.
    
    Uses Admin.can_manage_finances() to validate admin permissions.
    """
    # USE OOP METHOD: Admin.can_manage_finances() checks permissions
    admin = g.current_user
    if isinstance(admin, Admin) and not admin.can_manage_finances():
        raise ForbiddenError(
            f"Admin '{admin.get_display_name()}' does not have permission to manage finances. "
            f"Required: 'full' access level, Current: '{admin.access_level}'"
        )
    
    payload = PaymentStatusUpdate.model_validate(request.get_json(force=True))
    payment = payment_service.update_payment_status(payment_id=payment_id, status=payload.status)
    
    result = payment.to_dict()
    result['updated_by'] = admin.get_display_name()
    return result, HTTPStatus.OK

@payments_bp.route("/payments/<int:payment_id>", methods=["DELETE"])
@require_role('admin')
def delete_payment(payment_id: int):
    """Delete payment - Admin only.
    
    Uses Admin.can_manage_finances() to validate admin permissions.
    """
    # USE OOP METHOD: Admin.can_manage_finances() checks permissions
    admin = g.current_user
    if isinstance(admin, Admin) and not admin.can_manage_finances():
        raise ForbiddenError(
            f"Admin '{admin.get_display_name()}' does not have permission to manage finances. "
            f"Required: 'full' access level, Current: '{admin.access_level}'"
        )
    
    payment_service.delete_payment(payment_id)
    return {"deleted": True, "id": payment_id, "deleted_by": admin.get_display_name()}, HTTPStatus.OK
