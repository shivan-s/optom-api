"""Token schema relating to authentication."""

from pydantic import BaseModel


class Token(BaseModel):
    """Token Pydantic model."""

    access_token: str
    token_type: str
