from sqlalchemy import Column, Integer, String, DateTime, text
from .database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    time = Column(DateTime(timezone=True), nullable=False)
    location = Column(String(255))
    guests = Column(Integer, server_default="0", nullable=False)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text('now()'))
