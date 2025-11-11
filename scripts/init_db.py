"""Initialize database - create tables and first superuser."""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.db.session import init_db, engine
from app.db.base import Base
from app.services.auth_service import AuthService
from app.db.session import AsyncSessionLocal
from app.config import settings


async def create_tables():
    """Create all database tables."""
    print("Creating database tables...")

    async with engine.begin() as conn:
        # Drop all tables (use with caution!)
        # await conn.run_sync(Base.metadata.drop_all)

        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Tables created successfully!")


async def create_first_superuser():
    """Create first superuser from environment variables."""
    print(f"Creating superuser: {settings.FIRST_SUPERUSER_EMAIL}")

    async with AsyncSessionLocal() as db:
        auth_service = AuthService(db)

        try:
            # Check if superuser already exists
            existing = await auth_service.get_user_by_email(
                settings.FIRST_SUPERUSER_EMAIL
            )

            if existing:
                print("⚠️  Superuser already exists!")
                return

            # Create superuser
            user = await auth_service.create_superuser(
                email=settings.FIRST_SUPERUSER_EMAIL,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                full_name=settings.FIRST_SUPERUSER_NAME
            )

            print(f"✅ Superuser created: {user.email}")

        except Exception as e:
            print(f"❌ Error creating superuser: {e}")
            raise


async def main():
    """Run database initialization."""
    print("🚀 Initializing database...")
    print(f"📍 Database URL: {settings.DATABASE_URL.split('@')[1]}")  # Hide credentials

    try:
        await create_tables()
        await create_first_superuser()

        print("\n✅ Database initialization complete!")
        print(f"\nℹ️  Superuser credentials:")
        print(f"   Email: {settings.FIRST_SUPERUSER_EMAIL}")
        print(f"   Password: {settings.FIRST_SUPERUSER_PASSWORD}")
        print(f"\n⚠️  Change the superuser password in production!")

    except Exception as e:
        print(f"\n❌ Initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
