from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ClipModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    url: str = Field(..., min_length=1)
    start: str = Field(..., min_length=1)
    end: str = Field(..., min_length=1)
    filename: str = Field(..., min_length=1)

    @field_validator("start", "end")
    @classmethod
    def _validate_time_format(cls, value: str) -> str:
        try:
            datetime.strptime(value, "%H:%M:%S")
        except ValueError as e:
            raise ValueError("must be in HH:MM:SS format") from e
        return value
