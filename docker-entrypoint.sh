#!/bin/bash
set -e

case "$1" in
    "web")
        exec python run.py
        ;;
    "celery")
        exec celery -A backend.celery.celery_worker.celery worker --loglevel=info
        ;;
    *)
        exec "$@"
        ;;
esac
