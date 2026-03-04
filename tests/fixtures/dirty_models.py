"""Sample Pydantic models with multiple convention violations."""

from typing import Any

from pydantic import BaseModel


class BadModel(BaseModel):
    optional_field: str = "default"
    required_after_optional: str
    dataPayload: Any
    untyped = "no annotation"


class RegularClass:
    """This is a plain class, not a BaseModel. Should be skipped."""

    value = 42
