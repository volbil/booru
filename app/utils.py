from datetime import datetime, UTC
from functools import lru_cache
from dynaconf import Dynaconf
from datetime import timezone
import secrets
import bcrypt
import re


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
