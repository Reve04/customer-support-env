from pydantic import BaseModel, field_validator
from typing import Optional

class Observation(BaseModel):
    ticket_id: str
    subject: str
    body: str
    customer_tier: str
    account_age_days: int
    task_name: str

class Action(BaseModel):
    priority: str
    department: Optional[str] = None
    draft_response: Optional[str] = None

class Reward(BaseModel):
    score: float
    max_score: float = 0.99  # Never expose 1.0 as max to avoid boundary confusion
    feedback: str

    @field_validator("score", mode="before")
    @classmethod
    def clamp_score(cls, v):
        """Unconditionally enforce strict open interval (0, 1)."""
        return max(0.01, min(0.99, float(v)))