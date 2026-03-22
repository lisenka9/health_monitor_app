#!/usr/bin/env python3
"""CLI утилиты для административных задач"""

import sys
import argparse
import os
from app.core.logging import setup_logging, get_logger
from app.database import init_db, engine, Base 
from app.services.user_service import user_service
from app.schemas.user import UserCreate
from sqlalchemy import text

setup_logging()
logger = get_logger("health-monitor.cli")

def run_migrations():
    """Применение миграций базы данных"""
    logger.info("migration_started")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("migration_completed_successfully")
        return 0
    except Exception as e:
        logger.error("migration_failed", error=str(e))
        return 1

def create_admin_user(email: str, password: str, full_name: str = "Admin"):
    """Создание административного пользователя"""
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        from app.repositories.user_repository import user_repository
        existing = user_repository.get_by_email(db, email)
        if existing:
            logger.info("admin_user_already_exists", email=email)
            return 0
        
        user_data = UserCreate(
            email=email,
            password=password,
            full_name=full_name
        )
        user = user_service.create_user(db, user_data)
        logger.info("admin_user_created", user_id=user.id, email=user.email)
        return 0
    except Exception as e:
        logger.error("admin_user_creation_failed", email=email, error=str(e))
        return 1
    finally:
        db.close()

def check_migration_status():
    """Проверка статуса миграций"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
            ))
            tables = [row[0] for row in result]
            logger.info("migration_status", tables=tables)
        return 0
    except Exception as e:
        logger.error("migration_status_check_failed", error=str(e))
        return 1

def main():
    parser = argparse.ArgumentParser(description="Health Monitor CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    server_parser = subparsers.add_parser("server", help="Run main server")
    migrate_parser = subparsers.add_parser("migrate", help="Run database migrations")
    admin_parser = subparsers.add_parser("create-admin", help="Create admin user")
    admin_parser.add_argument("--email", required=True, help="Admin email")
    admin_parser.add_argument("--password", required=True, help="Admin password")
    admin_parser.add_argument("--full-name", default="Admin", help="Admin full name")
    status_parser = subparsers.add_parser("migration-status", help="Check migration status")
    
    args = parser.parse_args()
    
    if args.command == "server":
        import uvicorn
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
    
    elif args.command == "migrate":
        sys.exit(run_migrations())
    
    elif args.command == "create-admin":
        sys.exit(create_admin_user(args.email, args.password, args.full_name))
    
    elif args.command == "migration-status":
        sys.exit(check_migration_status())
    
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()