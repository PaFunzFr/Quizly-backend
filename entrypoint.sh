#!/bin/sh
set -e

echo "[entrypoint] Running Django setup..."

if [ "$DEBUG" = "False" ]; then
    echo "[entrypoint] Production mode: Erstelle cookies.txt ..."
    
    COOKIE_DIR=$(dirname "$COOKIE_PATH")
    mkdir -p "$COOKIE_DIR"

    echo -e "$YT_COOKIES" > "$COOKIE_PATH"

    echo "[entrypoint] Cookies file created at $COOKIE_PATH"
    cat "$COOKIE_PATH"
else
    echo "[entrypoint] DEBUG-Modus: cookies.txt wird nicht erstellt."
fi

# ---- collect staticfiles and migrate db ----
python manage.py collectstatic --noinput
python manage.py migrate

# ---- create superuser & guest user ----
python manage.py shell <<'PYCODE'
import os
from django.contrib.auth import get_user_model

User = get_user_model()

# ---- Superuser ----
admin_email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
admin_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpassword')
admin_username = os.environ.get('DJANGO_SUPERUSER_FULLNAME', 'Admin')

if not User.objects.filter(username=admin_username).exists():
    print(f"[entrypoint] Creating superuser '{admin_email}' ...")
    User.objects.create_superuser(username=admin_username, email=admin_email, password=admin_password)
    print(f"[entrypoint] Superuser '{admin_username}' created.")
else:
    print(f"[entrypoint] Superuser '{admin_username}' already exists.")

# ---- Guest User ----
guest_email = os.environ.get('DJANGO_GUEST_EMAIL', 'guest@videoflix.com')
guest_password = os.environ.get('DJANGO_GUEST_PASSWORD', 'guestpassword')
guest_username = os.environ.get('DJANGO_GUEST_FULLNAME', 'Guest User')

if not User.objects.filter(username=guest_username).exists():
    print(f"[entrypoint] Creating guest user '{guest_email}' ...")
    guest = User.objects.create_superuser(username=guest_username, email=guest_email, password=guest_password)
    guest.is_staff = False
    guest.is_superuser = False
    guest.save()
    print(f"[entrypoint] Guest user '{guest_username}' created.")
else:
    print(f"[entrypoint] Guest user '{guest_username}' already exists.")
PYCODE

# ---- run Gunicorn ----
echo "[entrypoint] Starting Gunicorn..."
exec gunicorn core.wsgi:application \
    --bind 0.0.0.0:8001 \
    --workers 3 \
    --threads 2 \
    --timeout 1800
