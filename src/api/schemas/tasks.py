from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.api.tools.data_generator import fake_en


class BaseTaskSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=3, max_length=100)
    description: str = Field(max_length=500)
    status: Literal["todo", "in_progress", "done"]
    due_date: date | None
    id: UUID
    owner_id: UUID
    created_at: datetime
    updated_at: datetime


class CreateTaskRequestSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=3, max_length=100, default_factory=fake_en.task_title)
    description: str = Field(default="", max_length=500)
    status: Literal["todo", "in_progress", "done"] = Field(default="todo")
    due_date: date | None = None


class CreateTaskResponseSchema(BaseTaskSchema):
    pass


class GetTasksQueryParamsSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["todo", "in_progress", "done"] | None = None
    q: str | None = None
    sort: Literal["created_desc", "created_asc", "due_date_asc"] = "created_desc"
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=50)


class PaginationSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: int
    limit: int
    total: int
    pages: int


class GetTasksResponseSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[BaseTaskSchema]
    pagination: PaginationSchema


class GetTaskResponseSchema(BaseTaskSchema):
    pass


class PatchTaskRequestSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(default=None, min_length=3, max_length=100)
    description: str = Field(default=None, max_length=500)
    status: Literal["todo", "in_progress", "done"] = None
    due_date: date | None = None


class PatchTaskResponseSchema(BaseTaskSchema):
    pass
