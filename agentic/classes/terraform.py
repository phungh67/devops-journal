from typing import Literal
from pydantic import BaseModel, Field

class TFFinding(BaseModel):
    severity: Literal["high", "med", "low"]
    line: int = Field(..., description="The exact line number of the issue")
    issue: str
    fix: str

class TerraformReview(BaseModel):
    decision: Literal["approve", "request_changes", "block"]
    findings: list[TFFinding] = Field(default_factory=list)