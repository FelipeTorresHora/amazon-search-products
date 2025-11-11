#!/bin/bash
# Apply Alembic migrations

set -e

cd "$(dirname "$0")/../backend"

echo "🚀 Applying database migrations..."

# Run migrations
alembic upgrade head

echo "✅ Migrations applied successfully!"
