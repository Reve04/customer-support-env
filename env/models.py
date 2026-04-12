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
    max_score: float = 1.0  # Reference 1.0 ensures relative performance is never 100%
    feedback: str

    @field_validator("score", mode="before")
    @classmethod
    def clamp_score(cls, v):
        """Unconditionally enforce strict open interval (0, 1)."""
        try:
            if v is None:
                return 0.5
            f = float(v)
            if f != f:  # NaN check
                return 0.5
            return float(max(0.05, min(0.95, f)))
        except (ValueError, TypeError):
            return 0.5