#!/bin/bash
# Create new Alembic migration

set -e

cd "$(dirname "$0")/../backend"

# Check if message provided
if [ -z "$1" ]; then
    echo "Usage: ./create_migration.sh 'migration message'"
    exit 1
fi

echo "📝 Creating new migration: $1"

# Create migration
alembic revision --autogenerate -m "$1"

echo "✅ Migration created successfully!"
echo "ℹ️  Review the migration file before applying"
echo "ℹ️  Apply with: ./apply_migrations.sh"
