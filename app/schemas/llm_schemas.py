from pydantic import BaseModel, Field
from typing import Optional, List, Literal

class ExtractedEntities(BaseModel):
    """
    Dynamic entities depending on the detected intent.
    Not all fields will be populated at the same time.
    """
    # For shopping
    items: Optional[List[str]] = Field(default_factory=list)
    
    # For calendar
    title: Optional[str] = None
    date: Optional[str] = Field(None, description="Format YYYY-MM-DD")
    time: Optional[str] = Field(None, description="Format HH:MM")
    duration_minutes: Optional[int] = None
    
    # For notes
    tags: Optional[List[str]] = Field(default_factory=list)
    content: Optional[str] = None

class RouterOutput(BaseModel):
    """
    The exact JSON structure the LLM must return.
    """
    intent: Literal["shopping", "calendar", "note"] = Field(
        description="The main category of the user request."
    )
    action: Literal["add", "remove", "read"] = Field(
        description="The action to perform."
    )
    entities: ExtractedEntities = Field(
        description="The extracted data variables."
    )
    reply_summary: str = Field(
        description="A short, friendly one-line confirmation for the user."
    )