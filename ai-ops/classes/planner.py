# unified classes for all related to log analyze functions
from typing import Literal
from pydantic import BaseModel, Field

Severity = Literal["critical", "high", "medium", "low", "none"]

class ErrorPattern(BaseModel):
    pattern: str = Field(..., description="Short label for this error")
    count: int = Field(..., ge=0)
    sample: int = Field(..., description="One log line, verbatim")

class Action(BaseModel):
    priority: Literal["high", "medium", "low"]
    description: str
    command: str | None = Field(None, description="Shell command if applicable")

class Triage(BaseModel):
    severity: Severity
    summary: str = Field(..., description="One sentence")
    error_pattern: list[ErrorPattern] = Field(default_factory=list)
    likely_causes: list[str] = Field(default_factory=list)
    actions: list[Action] = Field(default_factory=list)
    confidence: Literal["low", "medium", "high"]


