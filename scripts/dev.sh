#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
exec .venv/bin/uvicorn app.main:create_app --factory --reload --host 127.0.0.1 --port 8000
