"""
Administrative Account Management CLI
Provides secure command-line administration for Tekken 8 Esports Portal:
- Creates and updates admin accounts with salted bcrypt password hashing
- Manages 2FA TOTP activation and status
- Seeds initial master superadmin from environment variables
"""

import os
import sys
import argparse

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.orm import Session
from backend.app.database.session import engine, Base, SessionLocal
from backend.app.models.admin_user import AdminUser
from backend.app.core.security import hash_password, verify_password
from backend.app.core.config import settings


def init_admin_table():
    """Ensure admin_users table exists in database."""
    Base.metadata.create_all(bind=engine, tables=[AdminUser.__table__])


def create_or_update_superadmin(username, email, password, role="SuperAdmin"):
    """Creates or updates a superadmin user with bcrypt hashing."""
    init_admin_table()
    db: Session = SessionLocal()
    try:
        user = db.query(AdminUser).filter(
            (AdminUser.username == username) | (AdminUser.email == email)
        ).first()

        hashed = hash_password(password)

        if user:
            print(f"[!] Updating existing admin user: {user.username} (ID: {user.id})")
            user.username = username
            user.email = email
            user.password_hash = hashed
            user.role = role
            user.failed_login_attempts = 0
            user.locked_until = None
        else:
            print(f"[+] Creating new superadmin user: {username} ({email})")
            user = AdminUser(
                username=username,
                email=email,
                password_hash=hashed,
                role=role,
                totp_enabled=False,
                failed_login_attempts=0
            )
            db.add(user)

        db.commit()
        db.refresh(user)
        print(f"[SUCCESS] Admin account verified: ID={user.id}, Username={user.username}, Role={user.role}, 2FA={user.totp_enabled}")
        return user
    finally:
        db.close()


def list_admins():
    """Lists all admin accounts."""
    init_admin_table()
    db: Session = SessionLocal()
    try:
        users = db.query(AdminUser).all()
        print(f"\n{'ID':<4} {'Username':<18} {'Email':<30} {'Role':<12} {'2FA Enabled':<12} {'Last Login'}")
        print("=" * 85)
        for u in users:
            last_l = u.last_login.strftime('%Y-%m-%d %H:%M') if u.last_login else 'Never'
            print(f"{u.id:<4} {u.username:<18} {u.email:<30} {u.role:<12} {str(u.totp_enabled):<12} {last_l}")
        print("=" * 85)
        print(f"Total admin accounts: {len(users)}\n")
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="Tekken 8 Admin Management CLI")
    parser.add_argument("--create-superadmin", action="store_true", help="Create or seed Master SuperAdmin")
    parser.add_argument("--username", type=str, default=None, help="Admin username")
    parser.add_argument("--email", type=str, default=None, help="Admin email address")
    parser.add_argument("--password", type=str, default=None, help="Admin plaintext password (hashed on save)")
    parser.add_argument("--role", type=str, default="SuperAdmin", help="Role (SuperAdmin, Editor)")
    parser.add_argument("--list", action="store_true", help="List all registered admin users")

    args = parser.parse_args()

    if args.list:
        list_admins()
        return

    if args.create_superadmin or (args.username and args.password):
        username = args.username or settings.INITIAL_ADMIN_USER or "alpha"
        email = args.email or settings.INITIAL_ADMIN_EMAIL or "asadqaisar17@gmail.com"
        password = args.password or settings.INITIAL_ADMIN_PASSWORD or "Alpha_1122#"
        create_or_update_superadmin(username, email, password, args.role)
    else:
        # Default run: seed master admin from settings/.env
        username = settings.INITIAL_ADMIN_USER or "alpha"
        email = settings.INITIAL_ADMIN_EMAIL or "asadqaisar17@gmail.com"
        password = settings.INITIAL_ADMIN_PASSWORD or "Alpha_1122#"
        create_or_update_superadmin(username, email, password, "SuperAdmin")


if __name__ == "__main__":
    main()
