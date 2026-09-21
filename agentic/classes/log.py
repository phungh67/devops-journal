from typing import Literal
from pydantic import BaseModel, Field

Severity = Literal["critical", "high", "medium", "low", "none"]

class ErrorPattern(BaseModel):
    pattern: str = Field(..., description="A short label for this error")
    count: int = Field(..., ge=0)
    sample: str = Field(..., description="One line log, verbatim")

class Action(BaseModel):
    priority: Literal["high", "medium", "low"]
    description: str
    command: str | None = Field(None, description="Any shell commands if applicable")

class Triage(BaseModel):
    severity: Severity
    root_cause: str = Field(..., description="One sentence to summary the issue")
    error_pattern: list[ErrorPattern] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list, description="Verbatim snippet")
    actions: list[Action] = Field(default_factory=list)
    next_step: str = Field(..., description="One concrete kubectl or curl command")
    confidence: Literal["low", "medium", "high"]