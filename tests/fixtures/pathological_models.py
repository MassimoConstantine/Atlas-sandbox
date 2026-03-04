"""Pathological Pydantic models for stress-testing the model linter."""

from pydantic import BaseModel, Field, field_validator


# Test 1: Model with 50 fields — all clean
class FiftyFieldModel(BaseModel):
    """A model with 50 properly defined fields."""

    field_01: str
    field_02: str
    field_03: str
    field_04: str
    field_05: str
    field_06: str
    field_07: str
    field_08: str
    field_09: str
    field_10: str
    field_11: str
    field_12: str
    field_13: str
    field_14: str
    field_15: str
    field_16: str
    field_17: str
    field_18: str
    field_19: str
    field_20: str
    field_21: str
    field_22: str
    field_23: str
    field_24: str
    field_25: str
    field_26: int
    field_27: int
    field_28: int
    field_29: int
    field_30: int
    field_31: float
    field_32: float
    field_33: float
    field_34: float
    field_35: float
    field_36: bool
    field_37: bool
    field_38: bool
    field_39: bool
    field_40: bool
    field_41: str = ""
    field_42: str = ""
    field_43: str = ""
    field_44: str = ""
    field_45: str = ""
    field_46: int = 0
    field_47: int = 0
    field_48: int = 0
    field_49: int = 0
    field_50: int = 0


# Test 2: Model with no fields (empty body besides docstring)
class EmptyModel(BaseModel):
    """A model with no fields at all."""


# Test 3: Field with extremely long name (200 chars)
class LongNameModel(BaseModel):
    """A model with an extremely long field name."""

    a_very_long_field_name_that_goes_on_and_on_and_on_to_test_whether_the_linter_can_handle_extremely_long_snake_case_identifiers_without_crashing_or_producing_false_positives_padding_aaaa_bbbb_cccc_ddddd: str  # noqa: E501


# Test 4: Class inheriting from non-BaseModel — should be skipped
class SomeOtherBase:
    """A non-Pydantic base class."""


class NotPydantic(SomeOtherBase):
    value = 42
    camelCase = "should not be flagged"


# Test 5: Model with validator methods — validators should not be flagged
class ValidatorModel(BaseModel):
    """A model with field validators that should not trigger lint rules."""

    user_name: str
    age: int

    @field_validator("user_name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        """Validate that user_name is not empty."""
        if not v.strip():
            msg = "Name must not be empty"
            raise ValueError(msg)
        return v


# Test 6: Nested models — parent references child as field type
class ChildModel(BaseModel):
    """A child model used as a nested type."""

    child_name: str
    child_value: int


class ParentModel(BaseModel):
    """A parent model with a nested child model field."""

    parent_id: str
    child: ChildModel
    children: list[ChildModel] = Field(default_factory=list)


# Test 7: Model with Field(...) using alias, description, examples
class AliasModel(BaseModel):
    """A model using Field with alias, description, and examples."""

    user_id: str = Field(
        ...,
        alias="userId",
        description="The unique user identifier",
        examples=["usr-001", "usr-002"],
    )
    display_name: str = Field(
        ...,
        description="Human-readable display name",
    )
    score: float = Field(
        default=0.0,
        description="User score",
        examples=[1.5, 99.9],
    )
