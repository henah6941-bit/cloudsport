#!/bin/bash
set -e

echo "CloudSport DB Init"
echo "=================="

if [ -z "$DATABASE_URL" ]; then
  echo "Error: DATABASE_URL is not set. Copy .env.example to .env and configure it."
  exit 1
fi

echo "DATABASE_URL is set."

cd "$(dirname "$0")"
echo "Running alembic upgrade head..."
alembic upgrade head

echo "✓ Database initialized successfully."
