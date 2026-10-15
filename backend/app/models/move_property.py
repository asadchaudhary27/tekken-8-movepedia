from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class MoveProperty(Base):
    __tablename__ = "move_properties"

    id = Column(Integer, primary_key=True, index=True)
    move_id = Column(Integer, ForeignKey("moves.id"), nullable=False, index=True)
    property_type = Column(String(32), nullable=False, index=True)  # heat_burst, heat_engager, power_crush, tornado, homing, high_crush, low_crush, wall_crush, balcony_break
    value = Column(String(64), nullable=True)

    move = relationship("Move", back_populates="properties")
