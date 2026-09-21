from typing import Literal
from pydantic import BaseModel, Field

class GraphEdge(BaseModel):
    source: str
    target: str
    relationship: str = Field(..., description="e.g., depends_on, writes_to, routes_to")

class GraphSpec(BaseModel):
    title: str
    diagram_type: Literal["flowchart", "architecture", "stateDiagram"]
    nodes: list[str] = Field(..., description="List of entity names")
    edges: list[GraphEdge] = Field(default_factory=list)
    mermaid_code: str = Field(..., description="Valid raw Mermaid markdown diagram snippet")