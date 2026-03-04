"""Pydantic v2 models for Atlas pipeline schemas: TaskIntent and BuildPlan."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class TaskIntent(BaseModel):
    """Schema for a TaskIntent document used in Atlas pipeline runs."""

    schema_type: Literal["TaskIntent"]
    task_id: str
    intent_type: str
    scope: list[str]
    constraints: list[str]
    acceptance_criteria: list[str]
    estimated_effort: str
    confidence: int = Field(ge=1, le=5)


class BuildPlan(BaseModel):
    """Schema for a BuildPlan document used in Atlas pipeline runs."""

    schema_type: Literal["BuildPlan"]
    steps: list[str]
    files_to_create: list[str]
    files_to_modify: list[str] = Field(default_factory=list)
    files_not_to_touch: list[str]
    test_strategy: str
    dependencies: list[str] = Field(default_factory=list)
    stop_conditions: list[str] = Field(default_factory=list)


SCHEMA_REGISTRY: dict[str, type[BaseModel]] = {
    "TaskIntent": TaskIntent,
    "BuildPlan": BuildPlan,
}
