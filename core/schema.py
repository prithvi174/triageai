from pydantic import BaseModel , Field
# BaseModel — defines the shape/structure of your data and auto-validates it.
# Field — adds extra rules like "required", min/max, description.

from enum import Enum # Enum — restricts a value to a fixed set of allowed options.
# Pass anything outside these rules → Pydantic throws an error automatically.

class Category(str ,Enum):
    HARDWARE = "Hardware"
    SOFTWARE = "Software"
    NETWORK = "Network"
    ACCESS_ACCOUNT = "Access_Account"
    OTHER = "Other"

class Priority(str , Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class Team(str , Enum):
    IT_SUPPORT = "IT Support"
    NETWORK_OPS = "Network Ops"
    SECURITY = "Security"
    APP_SUPPORT = "App Support"

class TicketRequest(BaseModel): # It defines what the user must send to your API. When someone hits your endpoint, FastAPI automatically checks — did they send a ticket_text? Is it a string? If no → reject immediately, you never even reach your LLM code. Without BaseModel you'd have to manually write all those checks yourself.
    ticket_text: str = Field(..., description="Raw IT support ticket description") # just the raw ticket, required, no rules except must be a string

class TriageResult(BaseModel):
    category: Category # must be one of 5 enum values (Hardware, Software...)
    priority: Priority # must be one of your Priority enum values
    suggested_team: Team # must be one of your Team enum values
    confidence: float = Field(..., ge=0.0 , le=1.0) # 0.0 to 1.0, how sure the LLM is , Means confidence must be between 0.0 and 1.0 — because it's a probability score. If LLM returns 1.5 or -0.2, Pydantic rejects it automatically.
    reasoning: str = Field(..., description="Short justification for the classification") # short explanation of why it picked that category

 
