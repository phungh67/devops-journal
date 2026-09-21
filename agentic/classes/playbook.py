from typing import Literal
from pydantic import BaseModel, Field

class ComponentPlacement(BaseModel):
    component: str = Field(..., description="e.g., Redis Cache, Ingress Controller")
    target_tier: str = Field(..., description="e.g., Private Subnet, VPC Edge, DMZ")
    tool_recommended: str = Field(..., description="e.g., AWS ElastiCache, Traefik")
    justification: str

class ArchitecturePhase(BaseModel):
    phase: int
    title: str
    steps: list[str]
    rollback_strategy: str

class PlaybookPlan(BaseModel):
    architecture_summary: str
    components: list[ComponentPlacement] = Field(default_factory=list)
    phases: list[ArchitecturePhase] = Field(default_factory=list)
    tradeoffs: list[str] = Field(default_factory=list)