from typing import Annotated

from pydantic import BaseModel, StringConstraints

ConstrainedStr = Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]


class ClipModel(BaseModel):
    url: ConstrainedStr
    start: ConstrainedStr
    end: ConstrainedStr
    filename: ConstrainedStr
