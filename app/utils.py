from fastapi.responses import RedirectResponse
from fastapi import Request, Response
from datetime import datetime, UTC
from functools import lru_cache
from dynaconf import Dynaconf
from datetime import timezone
import secrets
import bcrypt
import math
import re


# FastAPI redirect
def redirect(request: Request, redirect_path: str):
    response = RedirectResponse(redirect_path)

    if "hx-request" in request.headers:
        response = Response("OK")
        response.headers["HX-Location"] = redirect_path

    return response


# Function to check whether tag is valid
def is_valid_tag_name(name):
    return re.match(r"^[a-zA-Z0-9_]+$", name) is not None


# Replacement for deprecated datetime's utcnow
def utcnow():
    return datetime.now(UTC).replace(tzinfo=None)


# Replacement for deprecated datetime's utcfromtimestamp
def utcfromtimestamp(timestamp: int):
    return datetime.fromtimestamp(timestamp, UTC).replace(tzinfo=None)


# Get bcrypt hash of password
def hashpwd(password: str) -> str:
    return bcrypt.hashpw(str.encode(password), bcrypt.gensalt()).decode()


# Check bcrypt password hash
def checkpwd(password: str, bcrypt_hash: str | None) -> bool:
    if bcrypt_hash:
        return bcrypt.checkpw(str.encode(password), str.encode(bcrypt_hash))

    return False


def new_token():
    """Genereate new random token"""

    return secrets.token_urlsafe(32)


@lru_cache()
def get_settings():
    """Returns lru cached system settings"""

    return Dynaconf(
        settings_files=["settings.toml"],
        default_env="default",
        environments=True,
    )


# Split list into chunks
def chunkify(lst, size):
    return [lst[i : i + size] for i in range(0, len(lst), size)]


# Convest timestamp to UTC datetime
def from_timestamp(timestamp: int):
    return utcfromtimestamp(timestamp) if timestamp else None


# Convert datetime to timestamp
def to_timestamp(date: datetime | None) -> int | None:
    date = date.replace(tzinfo=timezone.utc) if date else date
    return int(date.timestamp()) if date else None


# Helper function for pagination
def pagination(page, size=50):
    offset = (size * (page)) - size
    return size, offset


def frontend_pagination(page, items, count, path):
    total = math.ceil(count / items)
    pagination = range(page - 3, page + 4)
    pagination = [item for item in pagination if item >= 1 and item <= total]
    previous_page = page - 1 if page != 1 else None
    next_page = page + 1 if page != total else None

    return {
        "previous": previous_page,
        "pages": pagination,
        "next": next_page,
        "current": page,
        "total": total,
        "path": path,
    }
