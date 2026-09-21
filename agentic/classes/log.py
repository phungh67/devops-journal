from typing import Literal
from pydantic import BaseModel, Field

class Triage(BaseModel):
    root_cause: str = Field(
        ..., 
        description="One sentence summarizing the most likely root cause."
    )
    evidence: list[str] = Field(
        default_factory=list, 
        description="Verbatim log line snippets acting as evidence."
    )
    confidence: Literal["low", "medium", "high"]
    next_step: str = Field(
        ..., 
        description="One concrete kubectl or curl command for the next step."
    )