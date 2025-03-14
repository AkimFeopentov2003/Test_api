from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from database import Base

class Roll(Base):
    __tablename__ = "rolls"

    id = Column(Integer, primary_key=True, index=True)
    length = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)
    removed_at = Column(DateTime, nullable=True)

    __table_args__ = {'extend_existing': True}