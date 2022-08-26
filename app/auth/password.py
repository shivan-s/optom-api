"""Generating password."""

from .verify import get_pwd_context


def get_password_hash(password: str) -> str:
    """Provide a hashed password.

    Args:
        password (str): Password provided by user.

    Returns:
        str: Hashed password.

    """
    pwd_context = get_pwd_context()
    return pwd_context.hash(password)
