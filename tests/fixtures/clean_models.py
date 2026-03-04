"""Sample Pydantic models that follow all Atlas conventions."""

from pydantic import BaseModel, Field


class TaskRecord(BaseModel):
    """A record of a completed task."""

    task_id: str
    task_name: str
    status: str
    description: str = ""
    retry_count: int = 0


class PipelineConfig(BaseModel):
    """Configuration for an Atlas pipeline run."""

    pipeline_id: str
    run_mode: str
    max_retries: int = Field(default=3)
    verbose: bool = False


class NotABaseModel:
    """This is not a Pydantic model and should be ignored."""

    some_attribute = "value"
