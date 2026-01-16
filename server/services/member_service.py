import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from services.db import get_session
from services.exceptions import NotFoundError, DuplicateError
from models.member import Member
from config.constants import DEFAULT_MEMBER_STATUS
from utils.validators import normalize_email, sanitize_string


def hash_password(password: str) -> str:
    """Hash a password using PBKDF2-HMAC-SHA256.

    Returns:
        Hashed password in format: salt$hash (both base64 encoded)
    """
    salt = os.urandom(32)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend(),
    )

    key = kdf.derive(password.encode("utf-8"))

    salt_b64 = base64.b64encode(salt).decode("utf-8")
    key_b64 = base64.b64encode(key).decode("utf-8")
    return f"{salt_b64}${key_b64}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify a password against stored salt$hash."""
    try:
        salt_b64, key_b64 = stored_hash.split("$", 1)
        salt = base64.b64decode(salt_b64.encode("utf-8"))
        old_key = base64.b64decode(key_b64.encode("utf-8"))

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
            backend=default_backend(),
        )

        kdf.verify(password.encode("utf-8"), old_key)
        return True
    except Exception:
        return False


class MemberService:
    """Service class for managing member operations following OOP principles."""

    def __init__(self):
        """Initialize the MemberService."""
        pass

    def list_members(self):
        """Retrieve all members from the database."""
        session = get_session()
        try:
            members = session.query(Member).all()
            # Convert to dicts before closing session to avoid DetachedInstanceError
            members_list = [m.to_dict() for m in members]
            return members_list
        finally:
            session.close()

    def get_member(self, member_id: int) -> dict:
        """Get a specific member by ID."""
        session = get_session()
        try:
            member = session.query(Member).filter(Member.id == member_id).first()
            if not member:
                raise NotFoundError("Member not found")
            # Convert to dict before closing session to avoid DetachedInstanceError
            member_dict = member.to_dict()
            return member_dict
        finally:
            session.close()

    def create_member(self, full_name: str, email: str, phone: str, national_id: str, password: str) -> Member:
        """Create a new member."""
        email_norm = normalize_email(email)
        phone_norm = sanitize_string(phone)
        national_id_norm = sanitize_string(national_id)
        
        # Split full_name into first_name and last_name
        name_parts = full_name.strip().split(maxsplit=1)
        first_name = name_parts[0] if name_parts else full_name
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        session = get_session()
        try:
            if session.query(Member).filter(Member.email == email_norm).first():
                raise DuplicateError("Email already exists")

            if session.query(Member).filter(Member.national_id == national_id_norm).first():
                raise DuplicateError("National ID already exists")

            member = Member(
                first_name=first_name,
                last_name=last_name,
                email=email_norm,
                phone=phone_norm,
                national_id=national_id_norm,
                password_hash=hash_password(password),
                status=DEFAULT_MEMBER_STATUS.value,
            )

            session.add(member)
            session.commit()
            session.refresh(member)
            # Convert to dict before closing session to avoid DetachedInstanceError
            member_dict = member.to_dict()
            return member_dict
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def update_member(self, member_id: int, full_name=None, email=None, phone=None, status=None) -> Member:
        """Update an existing member."""
        session = get_session()
        try:
            member = session.query(Member).filter(Member.id == member_id).first()
            if not member:
                raise NotFoundError("Member not found")

            if email is not None:
                email_norm = normalize_email(email)
                if email_norm != member.email:
                    # Check if email is used by any OTHER member
                    existing = session.query(Member).filter(
                        Member.email == email_norm,
                        Member.id != member_id
                    ).first()
                    if existing:
                        raise DuplicateError("Email already exists")
                    member.email = email_norm

            if full_name is not None:
                # Split full_name into first_name and last_name
                name_parts = full_name.strip().split(maxsplit=1)
                member.first_name = name_parts[0] if name_parts else full_name
                member.last_name = name_parts[1] if len(name_parts) > 1 else ""

            if phone is not None:
                phone_sanitized = sanitize_string(phone)
                # Phone validation is already done by Pydantic schema
                member.phone = phone_sanitized

            if status is not None:
                member.status = status

            session.commit()
            session.refresh(member)
            # Convert to dict before closing session to avoid DetachedInstanceError
            member_dict = member.to_dict()
            return member_dict
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_member(self, member_id: int) -> None:
        """Delete a member from the database.
        
        Args:
            member_id: The ID of the member to delete
            
        Raises:
            NotFoundError: If member doesn't exist
        """
        session = get_session()
        try:
            member = session.query(Member).filter(Member.id == member_id).first()
            if not member:
                raise NotFoundError("Member not found")
            
            session.delete(member)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
