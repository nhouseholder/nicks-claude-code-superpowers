"""Shared model detection for GLM hooks. Import with: from detect_model import detect_model"""
import os
import json
import urllib.request


def detect_model():
    """Detect current model from CLAUDE_MODEL env var or proxy's /last-route."""
    model = os.environ.get("CLAUDE_MODEL", "")
    if not model:
        try:
            resp = urllib.request.urlopen("http://127.0.0.1:17532/last-route", timeout=1)
            data = json.loads(resp.read())
            model = data.get("model", "")
        except Exception:
            pass
    return model.lower()


def is_glm5():
    """Return True if currently running on GLM-5 (Haiku picker)."""
    return "haiku" in detect_model()
