from pydantic import BaseModel, Field
from typing import Literal

class TaskAnalysis(BaseModel):
    priority: Literal["High", "Medium", "Low"] = Field(description="Priority level of the task")
    status: Literal["Accepted", "Rejected", "Send to Mentor"] = Field(description="Status of the task")
    reason: str = Field(description="Brief reason for the decision (max 20 words)") 