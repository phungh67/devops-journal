import os
from typing import Optional, Literal

from ollama import chat
from ollama import ChatResponse

from pydantic import BaseModel

class Triagle(BaseModel):
    """Definition, templating for the response from the AI agent
    
    Contains must have, must satisfy and must not be null fields.
    Should be used in collaboration with token count to measure the effective of prompts.
    """

    root_cause: str
    confidence: Literal["low", "medium", "high"]
    next_step: str

def triagle_response(path_to_template: str, evidence_path: str) -> Triagle:
    """Return a chat response but strictly satisfy the Pydantic class
    
    To improve the effectiveness with a pre-define template and evidence,
    there are 2 arguments and must be passed to this function
    ---
    Arguments:
    path_to_template[string]: path to the JSON template, define role, system prompt, response structural.
    evidence_path[string]: path to evidence files, should be handle by reading and aggregating all.
    
    Return:
    A Triagle object with root_cause, confidence and next_step
    """
    
    