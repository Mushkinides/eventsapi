from datetime import datetime
from pydantic import BaseModel

class EventBase(BaseModel):
    title: str
    time: datetime
    location: str
    guests: int = 0
    description: str

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ReminderTime(BaseModel):
    minutes_before: int