# Vercel looks for a WSGI/ASGI "app" object in files under /api.
# This just re-exports the real Flask app defined in ../app.py so we
# don't have to duplicate any routes/logic.
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import app  # noqa: E402  (import after sys.path tweak)
