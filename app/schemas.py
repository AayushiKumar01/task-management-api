from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200, strict=True)
    description: str | None = None
    is_completed: bool = False
    
    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty or whitespace")

        return value



class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    is_completed: bool | None = None
    
    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty or whitespace")

        return value



class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime